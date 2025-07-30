# -*- coding: utf-8 -*-
"""geoplot module from the GeoDataKit: tools for ploting geoscience diagrams

This module mainly relies on advanced ploting libraries, which are called
in specific ways to produce scientific visualisation tailored to geoscience
needs. Datasets are also prepared and processed for making the diagram 
generation easier.

The libraries used here are:
    - matplotlib: this library is used as a backend for others (e.g., seaborn)
    or directly to develop new visualisation tools
    - seaborn: this specialised visualisation library for statistical views
    is the main entry point for static diagrams
    - plotly: this library based on top of plotly.js uses javascript for
    runing interactive plots in HTML based enviromnent. It is used when helpful
    to visualise interactive plots.

The implemented plots are defined in classes:
    - RoseDiagram: builds a plot for showing direction distributions
    
Helper functions provide direct access to the diagram generation:
    - rose_diagram(): generates a RoseDiagram
"""

from GeoDataKit.utils import get_kargs

import numbers
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

#------------------------------------------------------------------------------------------------
# Rose diagrams to show directions
def rose_diagram(data, **kargs):
    """
    Generates a RoseDiagram to show direction data.

    Parameters
    ----------
    data : :class:`pandas.DataFrame` or array-like data
        the dataset containing the direction data. Either passed as a DataFrame
        or as an array-like structure. If an array-like structure is used, then
        it must be passed as a single column array containing only the 
        direction data. If a DataFrame is used, the column containing the 
        directions must be specified by setting the column name in the 
        direction parameter. If using a DataFrame, optionally, a category
        can be associated with each entry. It must be described by another
        column in the DataFrame containing a string or integer corresponding to
        the classification; in this case, category parameter must receive the
        name of the corresponding column.
    **kargs: dict()
        keyword arguments passed to the `RoseDiagram` methods. Refer to the 
        documentation of this class to see the full list of arguments.
        
        
    Keyword arguments
    ---------------
    direction_label : str, optional
        Label of the column containing the direction data. Must be given if the
        dataset is passed as a DataFrame. The default is None.
    category_label : str, optional
        Label of the column containing a classification of the entries in the
        dataset. The default is None.
    degrees: bool, optional
        tells whether the data is in degrees or in radian.
        Default is True, meaning it is in degrees.
    bin_width: float, optional
        The width of the histogram bars in degrees if degrees is True,
        in radian otherwise. Default is 10.
    verbose: bool, optional
        Specify the behaviour of the class, whether it should
        output information or not. The default is False.

    Returns
    -------
    The created RoseDiagram object containing a rose diagram.

    """
    
    rose = RoseDiagram(data, **kargs )
    rose.show(**kargs)
    
    return rose

class RoseDiagram:
    """RoseDiagram: a polar histogram to analyse directional data
    
    A Rose diagram is a special kind of graphics used in geosciences
    for depicting the distribution of directions in a dataset.
    It is called Rose as a reference to the flower-like shape of the diagram.
    
    In this representation, the directions are separated into bins of small
    ranges of equal width and the number (or proportion) of entries falling 
    into each bin is represented by the length of a bar oriented in the 
    corresponding direction. This is very much like an histogram in polar
    coordinates. Each bar looks like a petal in a rose.
        
    Attributes
    -----------
    data: :class:`pandas.DataFrame`
        A Pandas DataFrame containing the direction dataset and categories
        if necessary.
    fig: Figure
        A Matplotlib Figure in which the diagram is drawn.
    ax: Axes
        A Matplotlib Axes in which the diagram is plotted
    
    Methods
    -----------
    set_data()
        set or updates the dataset
    show()
        Plots the Rose diagram
    """
    
    def __init__(self, data= None, **kargs ):
        """
        Constructor of a RoseDiagram.
        
        Parameters
        ----------
        data: :class:`pandas.DataFrame`, optional
            the dataset containing the orientation data.
            Orientation is expected to be expressed in degrees clockwise from
            North direction. The default is None as the data could be set later
            on by calling set_data().
            
        Keyword arguments
        ---------------
        direction_label : str, optional
            Label of the column containing the direction data. Must be given if the
            dataset is passed as a DataFrame. The default is None.
        category_label : str, optional
            Label of the column containing a classification of the entries in the
            dataset. The default is None.
        degrees: bool, optional
            tells whether the data is in degrees or in radian.
            Default is True, meaning it is in degrees.
        bin_width: float, optional
            The width of the histogram bars in degrees if degrees is True,
            in radian otherwise. Default is 10.
        verbose: bool, optional
            Specify the behaviour of the class, whether it should
            output information or not. The default is False.

        Returns
        -------
        None.

        """
        
        self.verbose = get_kargs("verbose", False, **kargs)
        if self.verbose: print("Preparing the data")
        
        degrees= get_kargs("degrees", True, **kargs)
        bin_width= get_kargs("bin_width", 10, **kargs)
        
        self.bin_width_rad = np.deg2rad(bin_width) if degrees else bin_width
        
        self.set_data(data, **kargs)
        
    def set_data(self, data, **kargs ):
        """
        Setter of dataset
        
        Parameters
        ----------
        data: :class:`pandas.DataFrame` 
            the dataset containing the orientation data.
            Orientation is expected to be expressed in degrees clockwise from
            North direction.
        direction_label : str, optional
            Label of the column containing the direction data. Must be given if
            the dataset is passed as a DataFrame. The default is None, if so 
            the first column with values is used.
        category_label : str, optional
            Label of the column containing a classification of the entries in the
            dataset. The default is None.
        degrees: bool
            tells whether the data is in degrees or in radian.
            Default is True, meaning it is in degrees.

        Returns
        -------
        None.

        """
        
        
        # processing the data
        if data is None:
            if self.verbose and (self.data is not None): print("Resetting the dataset.")
            self.data = data
            return
        assert( isinstance(data, pd.DataFrame)), "data must be a pd.DataFrame. Here data was: "+str(type(data))
        self.data = data
        
        # finding the direction label (either given or first value column)
        self.direction_label= get_kargs("direction_label", None, **kargs)
        if self.direction_label is None:
            self.direction_label = self.find_direction_label(self.data)
        
        self.category_label = get_kargs("category_label", None, **kargs)
        degrees= get_kargs("degrees", True, **kargs)
        
        # converting data from degrees to rad
        self.direction_label_rad = self.direction_label+"_rad" \
                                    if degrees and (self.direction_label is not None) \
                                    else self.direction_label
        if degrees and (self.data is not None):
            self.data[self.direction_label_rad] = np.deg2rad(self.data[self.direction_label]) 
        
    def find_direction_label(self,data):
        assert(not data.empty), "data must contain values, here data.empty is True"
        number_columns = [col for col in data.columns if isinstance(data[col].iloc[0], numbers.Number) ]
        assert(len(number_columns)>0), "data must contain at least one column with numbers, here none was found in data:\n"+str(data.head())
        return number_columns[0]
        
    def add_data(self, data, 
                 direction_label= None, category_label= None, 
                 category_name= None, 
                 degrees= True
                 ):
        """
        add a given dataset to the current one

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.
        direction_label : TYPE, optional
            DESCRIPTION. The default is None.
        category_label : TYPE, optional
            DESCRIPTION. The default is None.
        category_name : str, optional
            The default is None.
        degrees : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        
        # dataset if it is None
        if self.data is None:
            self.direction_label= direction_label if direction_label is not None else "strike_deg"
            columns = []
            if (category_name is not None) or (category_label is not None):
                self.category_label= category_label if category_label is not None else "category"
                category_name = category_name if category_name is not None else "Cat_1"
                columns += [self.category_label]
            self.data = pd.DataFrame(columns=columns)
        elif isinstance(data, pd.DataFrame):
            direction_label= direction_label if direction_label is not None else self.find_direction_label(data)
            assert (direction_label in data.columns), "direction_label must be a column header of the dataset, here {} is not in {}.".format(direction_label, data.columns)
            columns={direction_label:self.direction_label}
            
            if (category_name is not None) or (category_label is not None):
                category_label= category_label if category_label is not None else self.category_label
                category_name = category_name if category_name is not None else self.guess_category_name()
                columns[category_label]= self.category_label
            data.rename(columns=columns)
            
    def show(self, **kargs):
        """
        Plots the Rose diagram.
        
        Parameters
        -----------
        stat_type: str, optional
            specifies which kind of statistics should be used for the bars:
                count, percent, frequency, proportion, density.
                Default is count. The options are copied from seaborn:
            - `count`: show the number of observations in each bin
            - `frequency`: show the number of observations divided by the bin width
            - `probability`: or `proportion`: normalize such that bar heights sum to 1
            - `percent`: normalize such that bar heights sum to 100
            - `density`: normalize such that the total area of the histogram equals 1
        x_axis_label: str, optional
            specifies the label for the orientation (theta) axis. Default is
            the name of the column containing the orientation data.
        y_axis_label: str, optional
            specifies the label for the statistics (r) axis. Default is
            the text specified by default depending on the choice of stat_type.
            Use None to remove te label.
        y_axis_label_padding: int, optional
            padding to shift the location of the y axis label and avoid 
            intersection with the orientation labels. Default is 20.
            Only used when y_axis_label_location is left.
        y_axis_label_location: str, optional
            sets the location of the y_axis  label.
            -left: on the left of the diagram
            -north: along the North axis
            Default is left
        y_axis_angle: number, optional
            the location of the y_axis values, as an angle in degree. Default 0
        category_order: list, optional
            specifies the ordering of the categories to be plotted. The first 
            one is on top of the other and so on. Should give a list of 
            category namesDefault is None, i.e., keeps the default ordering.
        bin_shape: str, optional
            specifies the shape of the bins. Default is bars.
            -`bars`: each bin is an individual bar
            -`step`: all the bars in each category are gathered in a same shape
            -`poly`: a polygone is drawn for each category, producing a 
            smoother shape.
        category_interaction: str, optional
            specifies how different category should interact. Default `layer`
            - `layer`: each category is drawn in a different layer, visible by 
            transparency below those above.
            - `stack`: each category is drawn in the continuation of the 
            previous shape, stacking it in the radial direction.
            - `proportion`: the drawing will fill all the radial space and
            the proportion of each category is represented by the relative
            portion of the shape occupied by the category.
        edge_color: str, optional
            a matplolib color or string to specify the color of the edges of 
            the shapes.
        edge_width: float, optional
            the thickness of the shape edges. Use 0. to remove the edges.
            Default is 0.75
        color_palette: str; optional
            variations of the color palette to be used for categories. cf.,
            seaborn documentation:  deep, colorblind, bright, muted, dark,
            pastel. Default is bright.
        alpha: float, optional
            set the level of transparency. Default is 0.75.
        shrink: float, optional
            shrinking makes the bars smaller in width which better separates
            the bars for visualisation purpose. It is given as a factor of 
            contraction (shrink) between 1 (full width) and 0 (completely 
            collapsed). It only affects the "bars" layout (i.e., ignored for
            "step" and "poly". Default is 1. (i.e., no shrink).

        Returns
        -------
        None.

        """
        
        if self.verbose: print("Creating the diagram")
        self.fig = plt.figure()
        fig_size = get_kargs("fig_size", (14,8), **kargs)
        self.fig.set_size_inches(fig_size)
        self.ax = plt.axes(projection= "polar")
        # setting the theta orientation properly
        self.ax.set_theta_zero_location('N') # set the North up
        self.ax.set_theta_direction(-1) # set the angles clock-wise
        # add grid every 10 degree and North East South West main directions
        self.ax.set_thetagrids(angles=np.concatenate((np.arange(0, 360, 10), np.arange(0, 360, 90))),
                          labels=np.concatenate((np.arange(0, 360, 10), ["N","E","S","W"])))

        # parameters
        stat_type = get_kargs("stat_type","count",**kargs)
        bin_shape = get_kargs("bin_shape","bars",**kargs)
        category_order = get_kargs("category_order",None,**kargs)
        category_interaction = get_kargs("category_interaction","layer",**kargs)
        category_interaction = "fill" if category_interaction == "proportion" else category_interaction
        x_axis_label = get_kargs("x_axis_label",self.direction_label, **kargs)
        y_axis_label = get_kargs("y_axis_label","default", **kargs)
        y_axis_label_padding = get_kargs("y_axis_label_padding",20, **kargs)
        y_axis_label_location = get_kargs("y_axis_label_location","left", **kargs)
        y_axis_angle = get_kargs("y_axis_angle",0, **kargs)
        edge_color = get_kargs("edge_color","k", **kargs)
        edge_width = get_kargs("edge_width",0.75, **kargs)
        color_palette = get_kargs("color_palette","bright", **kargs)
        alpha = get_kargs("alpha",0.75, **kargs)
        shrink = get_kargs("shrink",1.0, **kargs)

        if self.data is None:
            if self.verbose: print("Undefined dataset, not drawing.")
        else:
            if self.verbose: print("Plotting the diagram")
                        
            self.binrange= [-self.bin_width_rad/2.0, 2*np.pi - self.bin_width_rad/2.0]

            self.data["dip_rad_phase"] = self.binrange[0] + (self.data[self.direction_label_rad] - self.binrange[0]) %(2*np.pi)

            # using seaborn for drawing the polar histogram
            sns_ax = sns.histplot(self.data,
                 x= "dip_rad_phase", hue= self.category_label,
                 binwidth= self.bin_width_rad, binrange= [-self.bin_width_rad/2.0,2*np.pi-self.bin_width_rad/2.0],
                 stat= stat_type,
                 hue_order= category_order if self.category_label is not None else None,
                 multiple= category_interaction,
                 element= bin_shape,
                 edgecolor= edge_color, linewidth= edge_width, zorder= 10,
                 palette= color_palette if self.category_label is not None else None,
                 alpha= alpha,
                 shrink= shrink,
                 ax= self.ax, legend= True )
            if self.category_label is not None:
                sns.move_legend(sns_ax, "upper left", bbox_to_anchor = (1.1, 1))
        
        r_ticks = self.ax.get_yticks()
        self.ax.set_rgrids( r_ticks, angle= y_axis_angle)
        if y_axis_label != "default":
            self.ax.set_ylabel(y_axis_label)
        self.ax.set_ylabel(self.ax.get_ylabel(),labelpad= y_axis_label_padding)
        if y_axis_label_location == "north":
            y_label_coord = get_kargs("y_label_coord", (0.5, 0.95), **kargs)
            self.ax.yaxis.set_label_coords(*y_label_coord)    
        self.ax.set_xlabel(x_axis_label)


# ------------------------------
# Hough
def get_key_argument(key,default,**kargs):
    """read a parameter from kargs dict (**kargs) given its key, if not found or kargs is None it returns the default value"""
    return default if key not in kargs.keys() else kargs[key]

class HoughKernel:
    def kernel(type="gaussian",**kargs):
        return kernel_dict[type](**kargs)
    
    def gaussian(sigma=1,**kargs):
        return lambda delta: np.exp(-0.5*(np.abs(delta)**2)/sigma**2)
    
    def triangle(sigma=1,trunc=True,**kargs):
        if trunc:
            return lambda delta: np.maximum(0,1 - np.abs(delta)/sigma)
        else:
            return lambda delta: 1 - np.abs(delta)/sigma
        
    def line(width,antialiase=True,**kargs):
        if antialiase:
            return lambda delta: np.where(np.abs(delta) < width/2, 1, np.maximum(0, 1 - (np.abs(delta)-width/2)/width*2))
        else:  
            return lambda delta: np.where(np.abs(delta) < width/2, 1, 0)

kernel_dict={
    "gaussian": HoughKernel.gaussian,
    "triangle": HoughKernel.triangle,
    "line": HoughKernel.line
}        

class HoughTransform:
    """This class describes a Hough Transformation to detect alignements in a point set.
    It holds a CartesianSpace where the data points are located and a HoughSpace that parameterises lines as a distance and an angle.
    """
    
    def __init__(self,data=None,**kargs):
        """Creates a new HoughTransform.
        
        data (optional [x,y], array of 2D points with x and y coordinates): if given it will help initialise the spaces, else you can give it later with add_data
        kargs (dict): optional arguments that will be passed along
        """
        self.vect = np.empty((0,2))
        self.distances = np.empty((0,1))
        self.center= np.array([0,0])
        self.cartesian = CartesianSpace(data,**kargs)
        self.hough = HoughSpace(self,**kargs)
        
        kargs["update_center"] = kargs["update_center"] if "update_center" in kargs.keys() else True
        self.add_data(data,**kargs)
        self.select_data_point(None)
        
    def add_data(self,data,update_center=True,**kargs):
        """adds data points to the Cartesian space
        data: array of x and y coordinates, [[x0,x1,...],[y0,y1...]]"""
        self.cartesian.add_data(data,**kargs)
        
        if update_center: self.update_center()

    def update_center(self,center=None):
        """ updates the HoughTransform center, default: uses the data set center if defined, else uses (0,0)"""
        self.center = center if center is not None \
                        else self.cartesian.center if self.cartesian.data is not None \
                        else np.array([0,0])
        self.update_vect()
        
    def update_vect(self):
        """computes the vectors from the hough center to the data points"""
        self.vect = self.cartesian.data.T - self.center if self.cartesian.data is not None else np.empty((0,2))
        self.update_distances()
            
    def update_distances(self):
        """computes the distances from hough center to data points"""
        self.distances = np.linalg.norm(self.vect,axis=1)
        self.hough.update_distance_array()
        
    def select_data_point(self,index=None):
        assert index is None or index < self.cartesian.data_length(), "index exceeds data count, {} > {}".format(index, self.cartesian.data_length())
        self.selected_index = index
        
    def line_normal(self,az):
        """Computes the normal vector to a line
        az: Azimuth of the line, angle in degrees, 0 means North, i.e., Y direction, increasing clockwise
        return: np.array([nx,ny]), with n the normal vector to the line
        if multiple az values are given, the returned form is np.array([[nx0,nx1...,nxn],[ny0,ny1,...nyn])"""
        
        az_rad = np.deg2rad(az)
        nx = -np.cos(az_rad)
        ny = np.sin(az_rad)
        return np.array([nx,ny])
    
    def line_vectors(self,az):
        """az: angle from North to the line in degrees (positive to the East)
        returns [[ux,uy],[vx,vy]] where u is the direction vector of the line and v its normal vector"""
        #az_rad = np.deg2rad(az)
        #ux = np.sin(az_rad)
        #uy = np.cos(az_rad)
        #return np.array([[ux,uy],[uy,-ux]])
        nx,ny= self.line_normal(az)
        return np.array([[-ny,nx],[nx,ny]])
    
    def compute_hough_distance(self,point,az):
        """computes the distances corresponding to a list of data points
        point ([x,y] or [[x0,y0],[x1,y1]...]): data points
        az (value or array): azimuth for which the distance must be evaluated
        returns: [dist], angle being the azimuth of the line and dist its distance to the hough center"""
        vect = point - self.center
        normal_vector = self.line_normal(az)
        return np.dot(vect,normal_vector)
    
    def compute_hough_point(self,point,az):
        """computes the angle and distances corresponding to a list of data points
        point ([x,y] or [[x0,y0],[x1,y1]...]): data points
        az (value or array): azimuth for which the distance must be evaluated
        returns: [x,y], coordinate of the hough point corresponding to the given line"""
        vect = point - self.center
        normal_vector = self.line_normal(az)
        return self.center + normal_vector * np.dot(vect,normal_vector)
    
    def hough_point(self,az,dist):
        normal_vector = self.line_normal(az)
        return self.center + normal_vector * dist
        
class CartesianSpace:
    """A class for describing a Cartesian space together with helper functions to handle it.
    Stores the data points."""
    
    def __init__(self,data=None,**kargs):
        """Creates a new CartesianSpace.
        
        data (optional [x,y], array of 2D points with x and y coordinates): if given it will help initialise the spaces, else you can give it later with add_data
        kargs (dict): optional arguments that will be passed along
        used arguments:
         - padding_perc (number, default 0.05): percentage of the data width to add to X and Y range to define the data region
        """
        self.add_data(data,**kargs)
        self.update_area(xmin=0,xmax=10,ymin=0,ymax=10,**kargs)
        
    def is_empty(self):
        """tells if the space is empty"""
        return self.data_length() == 0
    
    def data_length(self):
        return 0 if self.data is None else self.data.shape[-1]
        
    def add_data(self,data,update_area=False,**kargs):
        """adds data to the Cartesian space
        data ([x,y], array of 2D points with x and y coordinates) 
        kargs (dict): optional arguments that will be passed along
        """
        self.data = data if data is not None else np.empty((2,0))
        if update_area: self.update_area(**kargs)
        
    def update_area(self,**kargs):
        """Parameters: kargs (dict) may contain
        - padding_perc (number, default 0.05): percentage of the data width to add to X and Y range to define the data region
        - xmin (number): minimal value of X for the bounding box
        - xmax (number): maximal value of X for the bounding box
        - ymin (number): minimal value of Y for the bounding box
        - ymax (number): maximal value of Y for the bounding box
        """
        self.padding_perc = get_key_argument("padding_perc",0.05,**kargs)
        self.xmin,self.ymin = (0,0)
        self.xmax,self.ymax = (10,10)
        if not self.is_empty():
            self.xmin,self.ymin = np.min(self.data,axis=1)
            self.xmax,self.ymax = np.max(self.data,axis=1)
        self.xmin = get_key_argument("xmin",self.xmin,**kargs)
        self.xmax = get_key_argument("xmax",self.xmax,**kargs)
        self.ymin = get_key_argument("ymin",self.ymin,**kargs)
        self.ymax = get_key_argument("ymax",self.ymax,**kargs)
        
        min_point = np.array([self.xmin,self.ymin])
        max_point = np.array([self.xmax,self.ymax])
        self.center = np.mean(np.array([[self.xmin,self.xmax],[self.ymin,self.ymax]]),
                              axis=1
                             )
        self.xmin,self.ymin = self.center + (1+self.padding_perc) * (min_point - self.center)
        self.xmax,self.ymax = self.center + (1+self.padding_perc) * (max_point - self.center)
        self.x_range = self.xmax - self.xmin
        self.y_range = self.ymax - self.ymin
        self.mean_range = np.mean((self.x_range, self.y_range))
        
class HoughSpace:
    """A class for describing a Hough space together with helper functions to handle it."""
    
    def __init__(self,hough_transform,**kargs):
        """creates a HoughSpace associated to a HoughTransform
        hough_transform (required): a HoughTransform giving context to this Hough Space
        
        Angles are in degrees, distances are in the unit of the CartesianSpace associated to the HoughTransform."""
        self.hough_transform = hough_transform
        
        self.init_angle_array(**kargs)
        self.update_distance_array(**kargs)
        
        self.update_hough_lines()
        
    def init_angle_array(self,**kargs):
        """inits the boundaries and array of angles defining the HoughSpace"""
        self.angle_min = get_key_argument("angle_min",0,**kargs)
        self.angle_max =  get_key_argument("angle_max",360,**kargs)
        self.angle_step = get_key_argument("angle_step",3,**kargs)
        
        n_angle = int((self.angle_max - self.angle_min)/self.angle_step)
        self.angle_array = np.linspace(self.angle_min, self.angle_max, n_angle, endpoint=True)
        
    def update_distance_array(self,**kargs):
        """inits the boundaries and array of distance defining the HoughSpace"""
        padding_perc = get_key_argument("padding_perc",0.05,**kargs)
        max_dist = max(self.hough_transform.distances) if len(self.hough_transform.distances) > 0 else 10
        self.distance_min = (1+padding_perc)*get_key_argument("distance_min",-max_dist,**kargs)
        self.distance_max = (1+padding_perc)*get_key_argument("distance_max",max_dist,**kargs)
        
        if "distance_step" in kargs.keys():
            self.distance_step = kargs["distance_step"]
            n_distance = int((self.distance_max - self.distance_min)/self.distance_step)
        else:
            n_distance = get_key_argument("n_distance",100,**kargs)
            self.distance_step = (self.distance_max - self.distance_min)/n_distance
        self.distance_array = np.linspace(self.distance_min, self.distance_max, n_distance, endpoint=True)
        
        self.update_hough_lines()
        self.update_accumulator()
        
    def update_hough_lines(self):
        self.hough_lines_dist = self.hough_transform.compute_hough_distance(self.hough_transform.cartesian.data.T,self.angle_array)
    
    def update_accumulator(self, kernel_type="gaussian",sigma=None,antialiase=True,**kargs):
        self.accumulator_angle, self.accumulator_dist = np.meshgrid(self.angle_array, self.distance_array)
        self.accumulator = np.zeros_like(self.accumulator_angle)
        
        if sigma is None:
            sigma = self.hough_transform.cartesian.mean_range / 10
            
        max = get_key_argument("max",self.distance_max,**kargs)
        if "max" in kargs.keys(): del kargs["max"]
        
        width = get_key_argument("width",self.distance_step,**kargs)
        if "width" in kargs.keys(): del kargs["width"]
        
        kernel = HoughKernel.kernel(type=kernel_type, sigma=sigma, max= max, width= width, antialiase=antialiase, **kargs)
        for line_dist_i in self.hough_lines_dist:
            delta = np.abs(self.accumulator_dist - line_dist_i)
            self.accumulator += kernel(delta)
    
    def find_optimum(self):
        i_max= np.argmax(self.accumulator)
        n = len(self.angle_array)
        i_angle,i_dist = (i_max//n,i_max%n)
        self.optimum_angle = self.accumulator_angle[i_angle,i_dist]
        self.optimum_dist = self.accumulator_dist[i_angle,i_dist]
        return (self.optimum_angle,self.optimum_dist)
    
class HoughPlot:
    """Handles the plottign of a Hough Transform"""
    
    def __init__(self,hough_transform=None,data=None):
        assert isinstance(hough_transform,HoughTransform) or hough_transform is None, "hough_transform must be an object HoughTransform, here it is {}".format(type(hough_transform))
        self.hough_transform = hough_transform if hough_transform is not None else HoughTransform()
        if data is not None: self.hough_transform.add_data(data)
        self.fig, self.cartesian_ax, self.hough_ax = 3*[None]
    
    def plot(self,show_cartesian=True,show_hough=True, force_init=False, **kargs):
        if self.fig is None or force_init:
            self.init_figure(**kargs)
        if show_cartesian: self.plot_cartesian(**kargs)
        if show_hough: self.plot_hough(**kargs)
        
    def init_figure(self,show_cartesian=True,show_hough=True,**kargs):
        """creates the figure for drawing either the Cartesian or Hough Spaces or both (default)"""
        if show_cartesian and show_hough:
            self.fig, [self.cartesian_ax, self.hough_ax] = plt.subplots(ncols=2,nrows=1)
        elif show_cartesian:
            self.fig, self.cartesian_ax = plt.subplots(ncols=1,nrows=1)
            self.hough_ax = None
        elif show_hough:
            self.fig, self.hough_ax = plt.subplots(ncols=1,nrows=1)
            self.cartesian_ax =None
        fig_size = get_key_argument("fig_size",(16,6),**kargs)
        self.fig.set_size_inches(fig_size)
        
    def plot_cartesian(self, 
                       show_data= True,
                       show_selected= False,
                       show_center= False,
                       show_hough_center= True,
                       **kargs):
        """Plots the Cartesian space with all relevant information."""
        self.update_cartesian_axis(**kargs)
        if show_center: self.show_center(**kargs)
        if show_hough_center: self.add_marked_point(self.hough_transform.center, marked_text='H',**kargs)
        if show_data: self.plot_data_points(**kargs)
        if show_selected: self.plot_selected(**kargs)
            
    def update_cartesian_axis(self,**kargs):
        """Changes the axis where drawing is made for Cartesian space
        - ax (pyplot axis): if a pyplot axis is given, the space will be drawn in it, else default pyplot axis is used
        - kargs: alternatively an axis can be passed to the kargs and will be used if ax is None
        """
        default_ax = self.cartesian_ax if self.cartesian_ax is not None else plt.gca()
        self.cartesian_ax = get_key_argument("cartesian_ax",default_ax,**kargs)
        self.update_cartesian_plot_info(**kargs)
        
    def update_cartesian_plot_info(self,**kargs):
        self.cartesian_ax.set_title("Cartesian space")
        self.cartesian_ax.set_xlabel("X")
        self.cartesian_ax.set_xlim(self.hough_transform.cartesian.xmin,self.hough_transform.cartesian.xmax)
        self.cartesian_ax.set_ylabel("Y")
        self.cartesian_ax.set_ylim(self.hough_transform.cartesian.ymin,self.hough_transform.cartesian.ymax)
        self.cartesian_ax.set_aspect('equal')
        
    def plot_point(self,x,y,**kargs):
        """Plots points into the Cartesian space."""
        self.update_cartesian_axis(**kargs)
        
        self.cartesian_ax.scatter(x,y,**kargs)
    
    def show_center(self,**kargs):
        center_style = get_key_argument("center_style",'+',**kargs)
        center_color = get_key_argument("center_color",'gray',**kargs)
        center_text = get_key_argument("center_text",'O',**kargs)
        
        self.ax.scatter(*self.center, marker= center_style, c= center_color)
        self.ax.annotate(s= center_text, xy= self.center, xytext= self.center)
    
    def add_marked_point(self,point,**kargs):
        marked_style = get_key_argument("marked_style",'+',**kargs)
        marked_color = get_key_argument("marked_color",'gray',**kargs)
        marked_size = get_key_argument("marked_size",16,**kargs)
        marked_text = get_key_argument("marked_text",None,**kargs)
        marked_shift = get_key_argument("marked_shift",[0.01,0.01],**kargs)
        min_dimension = min(self.hough_transform.cartesian.x_range,self.hough_transform.cartesian.y_range)
        marked_shift_vector = min_dimension * np.array(marked_shift)
        
        self.cartesian_ax.scatter(*point, marker= marked_style, c= marked_color,s=marked_size)
        if marked_text is not None:
            self.cartesian_ax.annotate(text= marked_text, xy= point, xytext= point + marked_shift_vector)
            
    def add_segment(self,A,B,**kargs):
        segment = np.reshape([A,B],(2,2))
        self.cartesian_ax.plot(segment[:,0],segment[:,1],**kargs)
        
    def add_line_az(self,origin,az,**kargs):
        """Add a line to the graph area by finding its intersections with the borders.
        Parameters:
        - origin ([x,y]): a point along the line
        - az (angle in degree): the angle from North direction to the line, positive towards the Est 
        """
        az_rad = np.deg2rad(az)
        vect = np.array([np.sin(az_rad),np.cos(az_rad)])
        self.add_line(origin,vect,**kargs)
        
    def add_line(self,origin,vect,**kargs):
        """Add a line to the graph area by finding its intersections with the borders.
        Parameters:
        - origin ([x,y]): a point along the line
        - vect ([ux,uy]): the direction vector of the line
        """
        vect = np.array(vect)
        if vect[0] == 0:
            kmin = (self.hough_transform.cartesian.ymin - origin[1])/vect[1]
            kmax = (self.hough_transform.cartesian.ymax - origin[1])/vect[1]
        elif vect[1] == 0:
            kmin = (self.hough_transform.cartesian.xmin - origin[0])/vect[0]
            kmax = (self.hough_transform.cartesian.xmax - origin[0])/vect[0]
        else:
            ks = [
                (self.hough_transform.cartesian.ymin - origin[1])/vect[1],
                (self.hough_transform.cartesian.ymax - origin[1])/vect[1],
                (self.hough_transform.cartesian.xmin - origin[0])/vect[0],
                (self.hough_transform.cartesian.xmax - origin[0])/vect[0]
            ]
            kmin,kmax = np.sort(ks)[[1,2]]
        A = origin + kmin * vect
        B = origin + kmax * vect
        self.add_segment(A,B,**kargs)
        
    def plot_data_points(self,**kargs):
        size = get_key_argument("data_size",1,**kargs)
        color = get_key_argument("data_color","black",**kargs)
        self.plot_point(*self.hough_transform.cartesian.data,s=size,c=color)
    
    def plot_selected(self,index=None,az=None,show_circle=False,show_hough_point=False,show_triangle=False,
                      show_vector=False,**kargs):
        """Select a given Cartesian point and highlight it in Cartesian and Hough spaces.
        
        index [int, default=None]: the index of the selected point
        az [value, default=None]: the azimuth of a selected line going through the selected point
        show_circle [Bool, default=True]: if True shows the Hough Circle in Cartesian space (gathering all the possible poles for lines going through the selected point)
        show_hough_point [Bool, default=True]: if True shows the Hough pole for the selected point and line
        show_triangle [Bool, default=True]: if True shows the triangle in Cartesian space joining the selected point, hough pole and hough center
        show_vector [Bool, default=True]: if True, shows the direction and normal vectors to the selected line"""
        if index is not None: self.hough_transform.select_data_point(index)
        selected = self.hough_transform.selected_index
        if selected is None: return
        
        selected_point = self.hough_transform.cartesian.data[:,selected]
        selected_point_size = get_key_argument("selected_point_size",16,**kargs)
        selected_point_color = get_key_argument("selected_point_color","red",**kargs)
        selected_line_size = get_key_argument("selected_line_size",16,**kargs)
        selected_line_color = get_key_argument("selected_line_color","#69B9FB",**kargs)
        
        if self.cartesian_ax is not None:
            self.add_marked_point(selected_point,
                                  marked_size=selected_point_size, marked_color=selected_point_color,
                                  marked_text="P", marked_style= "o",zorder=10)
            
            if show_circle:
                circle_center = 0.5 * (selected_point + self.hough_transform.center)
                self.add_marked_point(circle_center, marked_color="gray", marked_text=None, marked_style= "+")
                self.add_segment(selected_point,self.hough_transform.center,linestyle='--',c="gray")
                circle_radius = np.linalg.norm(circle_center - self.hough_transform.center)
                circle = plt.Circle(circle_center, circle_radius, fill= False, linestyle='--')
                self.cartesian_ax.add_patch(circle)
                
            if az is not None:
                dir_vector,normal_vector = self.hough_transform.line_vectors(az)
                hough_point = self.hough_transform.compute_hough_point(selected_point,az)
                self.add_line_az(hough_point,az,c=selected_line_color)
                if show_hough_point:
                    self.add_marked_point(hough_point, marked_color="gray", marked_text="C", marked_style= "+")
                if show_triangle:
                    self.add_segment(self.hough_transform.center,hough_point,c="gray")
                    self.add_segment(selected_point,hough_point,c="gray")
                if show_vector:
                    self.cartesian_ax.annotate("", xytext=hough_point, xy=hough_point + dir_vector,
                                          arrowprops=dict(arrowstyle="->"))
                    self.cartesian_ax.annotate("", xytext=hough_point, xy=hough_point + normal_vector,
                                          arrowprops=dict(arrowstyle="->"))
            
        if self.hough_ax is not None:
            
            dist = self.hough_transform.compute_hough_distance(selected_point,az)
            self.hough_ax.scatter(az,dist,c=selected_line_color,s=selected_line_size,zorder=10,**kargs)
            self.hough_ax.scatter((az + 180)%360, -dist, c=selected_line_color,s=selected_line_size,zorder=10,**kargs)
            
            angle_array = self.hough_transform.hough.angle_array
            selected_line_dist = self.hough_transform.hough.hough_lines_dist[index]
            self.hough_ax.plot(angle_array,selected_line_dist,c=selected_point_color,zorder=5)
    
    def plot_hough(self,
                   show_accumulator= True,
                   show_lines= False,
                   **kargs):
        """Plots the Hough space with all relevant information."""
        self.update_hough_axis(**kargs)
        if show_accumulator: self.plot_hough_accumulator(**kargs)
        if show_lines: self.plot_hough_lines(**kargs)
        
    def plot_hough_lines(self,**kargs):
        angle_array = self.hough_transform.hough.angle_array
        for dist_array in self.hough_transform.hough.hough_lines_dist:
            self.hough_ax.plot(angle_array,dist_array)
            
    def plot_hough_accumulator(self, show_contour= False, show_optim=True, **kargs):
        extent = (self.hough_transform.hough.angle_min, self.hough_transform.hough.angle_max,
                  self.hough_transform.hough.distance_min, self.hough_transform.hough.distance_max)
        accumulator_mappable = self.hough_ax.imshow(self.hough_transform.hough.accumulator,origin="lower",extent=extent,aspect="auto",zorder=0)
        self.fig.colorbar(mappable=accumulator_mappable, ax=self.hough_ax)
        
        if show_contour:
            max_count = np.max(self.hough_transform.hough.accumulator)
            print(max_count)
            contour_mappable = self.hough_ax.contour(
                self.hough_transform.hough.accumulator_angle, self.hough_transform.hough.accumulator_dist,
                self.hough_transform.hough.accumulator, levels= np.arange(1,max_count,dtype=int),zorder=5,
                linestyles= ["solid"],
                colors= "darkgrey"
            )
            self.hough_ax.clabel(contour_mappable, inline=1, fontsize=10,colors="w",fmt="%d")
            
        if show_optim:
            self.hough_transform.hough.find_optimum()
            self.plot_manual(self.hough_transform.hough.optimum_angle,self.hough_transform.hough.optimum_dist)
            
    def update_hough_axis(self,**kargs):
        """Changes the axis where drawing is made for Hough space
        - ax (pyplot axis): if a pyplot axis is given, the space will be drawn in it, else default pyplot axis is used
        - kargs: alternatively an axis can be passed to the kargs and will be used if ax is None
        """
        default_ax = self.hough_ax if self.hough_ax is not None else plt.gca()
        self.hough_ax = get_key_argument("hough_ax",default_ax,**kargs)
        self.update_hough_plot_info(**kargs)
        
    def update_hough_plot_info(self,**kargs):
        self.hough_ax.set_title("Hough space")
        self.hough_ax.set_xlabel("Angle (degree)")
        self.hough_ax.set_xlim(self.hough_transform.hough.angle_min,self.hough_transform.hough.angle_max)
        self.hough_ax.set_ylabel("Distance")
        self.hough_ax.set_ylim(self.hough_transform.hough.distance_min,self.hough_transform.hough.distance_max)
        self.hough_ax.xaxis.set_ticks_position("both")
        self.hough_ax.yaxis.set_ticks_position("both")
        self.hough_ax.xaxis.set_ticks(range(0,365,45))
        self.hough_ax.xaxis.set_ticks(range(0,365,15),minor=True)
        self.hough_ax.set_aspect(2/3 / self.hough_ax.get_data_ratio())
        self.hough_ax.plot([self.hough_transform.hough.angle_min,self.hough_transform.hough.angle_max],[0,0],linewidth=1,linestyle='--',c="gray")
        
    def plot_manual(self,az,dist, color="red"):
        self.hough_ax.scatter(az,dist, zorder=10, c= color)
        self.hough_ax.scatter((az + 180)%360, -dist, zorder=10, c= color)
        
        hough_point = self.hough_transform.hough_point(az=az,dist=dist)
        self.add_line_az(hough_point,az, color=color)


#------------------------------------------------------------------------------------------------
# Principal Component Analysis
import sklearn as skl

def correlation_matrix(data, n_round= 2, cmap= "RdBu", ax= None, return_object= False):
    """Show correlation matrix

    :param data: the dataset
    :type data: a pandas DataFrame or a numpy array
    :param n_round: number of decimal digits, defaults to 2
    :type n_round: int, optional
    :param cmap: colormap to be used, defaults to "RdBu"
    :type cmap: str, optional
    :param ax: if this should be integrated into an existing plot you can pass it as ax,
    defaults to None, if None, a new graphics is created
    :type ax: a pyplot axis, optional
    :param return_object: if true the graphics is retruned, defaults to False
    :type return_object: bool, optional
    :return: the graphical object if return_object else None
    :rtype: a pyplot heatmap
    """    
    ax = ax if ax is not None else plt.gca()
    corr = data.corr() if isinstance(data, pd.DataFrame) else np.corrcoef(data, rowvar=False)
    matrix = corr.round(n_round)
    heatmap= sns.heatmap(matrix, annot=True, vmin=-1, vmax=1, cmap=cmap, ax= ax)
    ax.set_aspect("equal")
    if return_object:
        return heatmap
		
#Définition de fonctions pour l'ACP
def pc_names(pca= None, n_components= None, comp_basename= None):
    """Generates the names for Principal components

    :param pca: a principal component analysis or linear discriminant analysis object, defaults to None
    :param n_components: _description_, defaults to None
    :type n_components: _type_, optional
    :param comp_basename: _description_, defaults to None
    :type comp_basename: the basename to be used, if not given it is PC for PCA LD for LDA, optional
    :return: the names
    :rtype: list of names
    """    
    assert(pca != None or n_components != None), "At least one of pca or n_components should be given"
    
    if isinstance(pca, skl.decomposition.PCA):
        comp_basename= comp_basename if comp_basename is not None else "PC"
        n_components = pca.n_components_
    elif isinstance(pca, skl.discriminant_analysis.LinearDiscriminantAnalysis):
        comp_basename= comp_basename if comp_basename is not None else "LD"
        n_components = pca.scalings_.shape[1]
    else:
        raise("Unsupported type of space reduction", type(pca))
        
    return [comp_basename+str(i+1) for i in range(n_components)]

def plot_explained_variance(pca, ax= None, comp_names = None, fig_size= None):
    ax = ax if ax is not None else plt.gca()
    ratios = pca.explained_variance_ratio_
    comp_names = comp_names if comp_names is not None else pc_names(pca) 
    sns.barplot(x=comp_names, y=ratios, color="lightblue", ax=ax)
    ax = ax.twinx()
    ax.set_ylim((0,1.05))
    sns.lineplot(x=comp_names, y=ratios.cumsum(), color="red", ax=ax)
    ax.set_title("Explained Variance")
    if fig_size is not None:
        plt.gcf().set_size_inches(fig_size)
    
def plot_correlation_circle(pca,
                            var_names,
                            ax= None, 
                            comp_id_x= 0, comp_id_y= 1,
                            label_shift = 0.08, arrow_width = 0.014, pc_arrow_width= 0.014,
                            circle_args = dict(edgecolor="k", fill=False, linewidth = 2),
                            font_args = dict(fontsize="large", fontfamily="cursive"),
                            arrow_args  = dict(fill=True, edgecolor="k", linewidth=0, facecolor="k"),
                            fig_size= None,
                            return_graphics= False
                           ):
    ax = ax if ax is not None else plt.gca()
    
    if isinstance(pca, skl.decomposition.PCA):
        kind = "pca"
    elif isinstance(pca, skl.discriminant_analysis.LinearDiscriminantAnalysis):
        kind = "lda"
    else:
        raise("Unsupported type of space reduction", type(pca))
    
    if kind == "pca":
        delta = 0.2
        ax.set_xlim((-1-delta,1+delta))
        ax.set_ylim((-1-delta,1+delta))
        ax.xaxis.set_major_formatter(lambda x, pos:'{:.1f}'.format(x))
        ax.yaxis.set_major_formatter(lambda y, pos:'{:.1f}'.format(y))
        corr_circle = plt.Circle((0,0), radius = 1, **circle_args)
        ax.add_patch(corr_circle)
        ax.set_title("Correlation Circle")
    ax.set_aspect("equal")
    
    if fig_size is not None:
        plt.gcf().set_size_inches(fig_size)

    for i, el in enumerate(var_names):
        
        if kind == "pca":
            components = pca.components_
        elif kind == "lda":
            components = pca.scalings_.T
        
        dx, dy = components[[comp_id_x,comp_id_y],i]
        ax.arrow(0,0,dx,dy, length_includes_head=True, width = arrow_width, **arrow_args )

        xy = np.array([dx,dy])
        label_position = xy + label_shift * xy/np.linalg.norm(xy)
        ax.text(*label_position,el,horizontalalignment="center", verticalalignment="center", **font_args )
        
    comp_names = pc_names(pca)
    ax.arrow(0,0,1,0, length_includes_head=True, width = pc_arrow_width*1.25, **arrow_args )
    ax.arrow(0,0,0,1, length_includes_head=True, width = pc_arrow_width*1.25, **arrow_args )
    ax.text(1.1, 0, comp_names[comp_id_x], horizontalalignment="center", verticalalignment="center", **font_args )
    ax.text(0, 1.06, comp_names[comp_id_y], horizontalalignment="center", verticalalignment="center", **font_args )

    if return_graphics: return ax
    
def plot_principal_components(pca, data,
                              x = None, y= None,
                              kind= "scatter", sampling= None, nbins= 40,
                              s=5, marker="*",
                              ax= None,
                              fig_size= None,
                              return_graphics= False, **kargs):
    ax = ax if ax is not None else plt.gca()
    ax.set_title("Individual Space")
    
    if x is None or y is None:
        if isinstance(pca, skl.decomposition.PCA):
            comp_names = ["PC"+str(i+1) for i in range(pca.n_components_)]
        elif isinstance(pca, skl.discriminant_analysis.LinearDiscriminantAnalysis):
            comp_names = ["LD"+str(i+1) for i in range(pca.scalings_.shape[1])]
        x = x if x is not None else comp_names[0]
        y = y if y is not None else comp_names[1]
    
    if sampling is not None:
        data = data.sample(n=sampling)
    if kind == "scatter":
        sns.scatterplot(data=data, x= x, y=y, ax=ax, **kargs)
    elif kind == "kde":
        sns.kdeplot(data=data, x= x, y=y, ax=ax, **kargs )
    elif kind == "hist":
        if not( ("bins" in kargs.keys()) or ("binwidth" in kargs.keys()) ):
            xmin, xmax = data[x].min(), data[x].max()
            xrange = xmax - xmin
            ymin, ymax = data[y].min(), data[y].max()
            yrange = ymax - ymin
            binwidth = max( xrange/nbins, yrange/nbins)
            sns.histplot(data=data, x= x, y=y, ax=ax, binwidth=binwidth, **kargs )
        sns.histplot(data=data, x= x, y=y, ax=ax, **kargs )
    ax.set_aspect("equal")
    if fig_size is not None:
        plt.gcf().set_size_inches(fig_size)
        
    if return_graphics: return ax

# ------------------------------

# script usage
if (__name__ == '__main__'):
    import GeoDataKit.dataset as dataset
    data = dataset.get_dataset("orientation")
    rose_diagram(data, category_label="category", bin_width=20,
                 color_palette= "bright",
                 category_order= ["Rand","Cat1","Cat2"],
                 stat_type= "density",
                 x_axis_label= "Orientation (°)",
                 y_axis_label_location= "north")

