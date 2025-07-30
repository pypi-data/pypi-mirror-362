##################################################################
#                                                                #
#.#####...#####...##..##..##..##...####...##......######...####..#
#.##..##..##..##...####...###.##..##......##......##......##.....#
#.#####...#####.....##....##.###..##.###..##......####.....####..#
#.##......##..##....##....##..##..##..##..##......##..........##.#
#.##......##..##....##....##..##...####...######..######...####..#
#................................................................#
#                                                                #
# PlanetaRY spanGLES                                             #
#                                                                #
##################################################################
# License http://github.com/seap-udea/pryngles-public            #
##################################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# External required packages
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

from pryngles import *

import spiceypy as spy
import numpy as np
from copy import deepcopy
from anytree import NodeMixin,RenderTree


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class Body
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
class Body(Orbody):
    """
    This is the class to create a general body in `pryngles`.

    Note
    -----
    This class is not intended to be used independently, just for inheritance purposes.

    Parameters
    ----------
    kind : `str`
        One of the kind of bodies defined in the package (:any:`consts.BODY_KINDS`)

    defaults : `OrderedDict`, `dict`
        Dictionary with the properties of the object (:any:`consts.BODY_DEFAULTS`)

    parent: :data:`~ body.Body`
        Object in the center of the orbit of this body.

    **properties: `dict`
        Specify additional body properties and its values from :any:`consts.REBOUND_ORBITAL_PROPERTIES` or :any:`consts.BODY_DEFAULTS`

    Returns
    -------
    :
        output : :data:`~ body.Body`
            Body object containing the physical, orbital and optical parameters for an astropyshical body

    Raises
    ------
    AssertionError
        If **parent** parameter is not a valid :data:`~ body.Body` object

    Attributes
    ----------
    sg : :any:`spangler.Spangler`
        Abbreviation of `spangler`. This is one of the most important objects in ``pryngles``. 
        It contains the :data:`~ spangler.Spangler` object in wich we sample and discretize the surface of the :data:`~ body.Body` object in order to compute light-matter interactions.
        | **Default** is ``None``.

    childs, children: `dict, tuple` 
        It contains child bodies (bodies which is having this body) as the center.

    See Also
    -------------
    :any:`spangler.Spangler`
        Visit our :doc:`spangler` reference to detailed explanation of the class and its purposes.

    Examples
    --------
    This brief example shows how to create a bodies system with a primary body

    >>> # Create a body with None parent and name = 'B'
    >>> B = pr.Body(kind = "Body", defaults = pr.BODY_DEFAULTS, parent = None, name='B')
    >>> # Create a body having parent the Body "B" defined before:
    >>> C = pr.Body(kind = "Body", defaults = BODY_DEFAULTS, parent = B, name="C")
    """

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Bassic methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    def __init__(self,kind,defaults,parent,**props):

        #Kind, parent and child attributes
        self.kind=kind
        self.__defaults=defaults
        
        #Prepare key attributes
        self.sg=None

        #Name of the object
        if 'name' in props:
            name=self.name=str(props["name"])
        elif 'name_by_kind' in props:
            name=self.name=self.kind
        else:
            name=self.name=str(hash(self))

        #Legacy
        if 'primary' in props:
            parent=props["primary"]
        if 'optics' in props:
            props.update(props["optics"])
        if 'orbit' in props:
            props.update(props["orbit"])
        if 'physics' in props:
            props.update(props["physics"])

        #Update childs and parent
        if parent is not None:
            if not isinstance(parent,Body):
                raise AssertionError(f"Parent is not a valid Object: {type(parent)}, {isinstance(parent,Body)}")
            else:
                self.parent=parent
                parent._update_childs(self)

        #Update parent and childs        
        self._update_parent(parent)
        self._update_childs()

        #Update default properties
        self.__dict__.update(defaults)
        #Set name
        self.name=name
        #Update body
        self.update_body(**props)
    
    def update_body(self,**props):
        """
        Update properties of the Body.
        
        Parameters
        ----------------------
        **props: dictionary:
            Properties to update.
            The current object is updated with new values provided in this new object
                
        Examples
        ---------------
        >>> # Let's create a Body first
        >>> B = pr.Body(kind = "Body", defaults = pr.BODY_DEFAULTS, parent = None, name='B')
        >>> # This only update the Body mass attribute.
        >>> B.update_body(m=2)
        """
        for prop in props:
            if prop in self.__defaults or prop in REBOUND_ORBITAL_PROPERTIES:
                self.__dict__[prop]=props[prop]
            else:
                raise ValueError(f"Property {prop} not identified in object {self.kind}")
                
        self.elements={k:v for k,v in self.__dict__.items() if k in REBOUND_ORBITAL_PROPERTIES}
        
        verbose(VERB_VERIFY,"Updating Body")
        self._update_properties()
    
    def _update_childs(self,child=None):
        if 'childs' not in self.__dict__:
            self.childs=dict()
        if child is not None:
            verbose(VERB_VERIFY,f"Add child {child.name} to body {self.kind} ({self.name})")
            self.childs[child.name]=child
            
    def _update_parent(self,parent=None):
        if 'parent' not in self.__dict__:
            if parent:
                verbose(VERB_VERIFY,f"Add parent {parent.name} to body {self.kind} ({self.name})")
            self.parent=parent
        elif parent is not None:
            verbose(VERB_VERIFY,f"Add parent {parent.name} to body {self.kind} ({self.name})")
            self.parent=parent
            parent._update_childs(self)
    
    def _update_properties(self):
        verbose(VERB_VERIFY,"Updating properties of Body")
        #Rotational angular velocity
        self.wrot=2*np.pi/self.prot
        #Rotation axis
        self.n_equ=sci.cartesian([1,self.roll,90*Consts.deg-self.i])
    
    def show_tree(self):
        print(RenderTree(self))
        

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Tested methods from module file body
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def spangle_body(self):
        """
        Spangle the surface of the body. It creates and updates the :data:`~ spangler.Spangler` object in wich we 
        generate a sampling for the discrete units (`Spangles`) over the whole area on the body

        Examples
        --------
        >>> # Once we Spangle the Body, we can access to its most importante atribute
        >>> B.spangle_body()
        >>> # The data attribute is a pandas DataFrame object
        >>> # It contains all the geometrical and state data that caracterize the body surface
        >>> B.sg.data
            name  spangle_type  geometry  scale                              n_equ  alpha_equ  ...   emit  above illuminated  transmit  transit  occult
        0      B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        1      B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        2      B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        3      B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        4      B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        ..   ...           ...       ...    ...                                ...        ...  ...    ...    ...         ...       ...      ...     ...
        982    B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        983    B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        984    B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        985    B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False
        986    B             6         1    0.1  [6.123233995736766e-17, 0.0, 1.0]          0  ...  False  False        True     False    False   False

        See Also
        --------------
        :any:`consts.SPANGLER_COLUMNS`
            To see a description for each column in the data attribute
        """
        
        #Create spangler
        self.sg=Spangler(
            nspangles=self.nspangles,
            name=self.name,
            n_equ=self.n_equ,
            alpha_equ=self.alpha,
            w=self.wrot,
            q0=self.q0,
        )
        
        #Populate spangler
        self.sg.populate_spangler(
            shape=self.shape,
            spangle_type=self.spangle_type,
            scale=self.radius,
            seed=self.seed,
            preset=self.preset,
            **self.geometry_args,
        )
        
        #Additional properties in the Spangler DataFrame
        if self.kind=="Star":
            self.sg.data.source=True
        
        self.sg.set_observer()
        self.sg.set_luz()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class Star
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Star(Body):
    """It creates a :data:`~ body.Star` object for self-luminous objects with emission properties.

    Parameters
    --------------------
    parent: :data:`~ body.Star`, `None`
        Body for wich Star is orbiting. 
        For ``None`` it means Star is the main body in the system
        | **Default** is ``None``.
        
    **props: `dict`
        Specify additional Star properties and its values. 
        For the complete set of default values of the properties see :any:`consts.STAR_DEFAULTS`

    Returns
    -------
    :
        output : :data:`~ body.Star`
            Star body object containing the physical, orbital and optical parameters.

    Raises
    ------
    ValueError
        If **parent** parameter is not a valid :data:`~ body.Star` object.
        Only another :data:`~ body.Star` can be the parent of a :data:`~ body.Star`
    """
    def __init__(self,
                 parent=None,
                 **props
                ):
        
        #Instantiate object with basic properties
        Body.__init__(self,"Star",STAR_DEFAULTS,parent,**props)

        #Check parent
        if self.parent is not None:
            if self.parent.kind!="Star":
                raise ValueError(f"Only another Star can be the parent of a Star (you provided {self.parent.kind})")

        self._update_star_properties()
        
    def _update_star_properties(self):

        verbose(VERB_VERIFY,"Updating properties of Star")
        
        #Compute limbdarkening at r = 0 to initialize normalization constant
        sci.limb_darkening(0,self.limb_coeffs)
        
        #Store limb darkening normalization
        self.norm_limb_darkening=SCIENCE_LIMB_NORMALIZATIONS[hash(tuple(self.limb_coeffs))]
        
    def update_star(self,**props):
        """General and specific update properties of the Star
        
        Parameters
        ----------------------
        **props: dictionary:
            Properties to update.
            The current object is updated with new values provided in this new object

        Attributes
        -------------------------
        limb_coeffs: `list, array`
            Limb darkening coefficients [2]. Its lenght defines the model to implement [1].

        norm_limb_darkening: `float`
            Limb darkening function normalization.

        References
        ---------------
        [1] Models for Limb-Darkening: https://pages.jh.edu/~dsing3/David_Sing/Limb_Darkening.html
        [2] Coefficients available at: https://pages.jh.edu/~dsing3/LDfiles/LDCs.CoRot.Table1.txt
        """
        verbose(VERB_VERIFY,"Updating star")
        
        Body.update_body(self,**props)
        self._update_star_properties()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class Planet
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Planet(Body):
    """
    It creates a :data:`~ body.Planet` object for non-luminous orbiting bodies with specific orbital
    parameters and surface characteristics (in ``pryngles``, `Moons` are constructed as planets)

    Parameters
    --------------------
    parent: :data:`~ body.Star`
        Body for wich Planet is orbiting.
        
    **props: `dict`
        Specify additional Planet properties and its values. 
        For the complete set of default values of the properties see :any:`consts.PLANET_DEFAULTS`

    Returns
    -------
    :
        output : :data:`~ body.Planet`
            Planet body object containing the physical, orbital and optical parameters

    Raises
    ------
    ValueError
        If `parent =  None`. Parent not provided and it is mandatory for :data:`~ body.Planet` object.
    """
    
    def __init__(self,
                 parent=None,
                 **props
                ):
        
        
        #Instantiate object with basic properties
        Body.__init__(self,"Planet",PLANET_DEFAULTS,parent,**props)
        
        #Check parent
        if self.parent is None:
            raise ValueError(f"Parent not provided and it is mandatory for {self.kind}.")
        
        #Update properties
        self.update_planet(**props)

    def _update_planet_properties(self):
        verbose(VERB_VERIFY,"Updating Planet properties")
        
    def update_planet(self,**pars):
        """General and specific update properties of the `Planet`
        
        Parameters
        ----------------------
        **props: dictionary
            Properties to update.
            The current object is updated with new values provided in this new object
        """

        verbose(VERB_VERIFY,"Updating Planet")
        Body.update_body(self,**pars)
        self._update_planet_properties()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class Ring
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Ring(Body):
    """
    It creates a :data:`~ body.Ring` object for particulate systems with unique optical and physical ring properties

    Parameters
    --------------------
    parent: :data:`~ body.Star`, :data:`~ body.Planet` 
        Body for wich Ring was formed around. If parent is Star type, it means a circumplanetary disk
        
    **props: `dict`
        Specify additional Ring properties and its values. 
        For the complete set of default values of the properties see :any:`consts.RING_DEFAULTS`

    Returns
    -------
    :
        output : :data:`~ body.Ring`
            Ring body object containing the physical, orbital and optical parameters

    Raises
    ------
    ValueError
        If `parent =  None`. Parent not provided and it is mandatory for :data:`~ body.Ring` object.           
    """

    def __init__(self,
                 parent=None,
                 **props
                ):
        
        
        #Instantiate object with basic properties
        Body.__init__(self,"Ring",RING_DEFAULTS,parent,**props)
        
        #Check parent
        if self.parent is None:
            raise ValueError(f"Parent not provided and mandatory for {self.kind}.")
        
        #Update properties
        self.update_ring(**props)

    def _update_ring_properties(self):
        verbose(VERB_VERIFY,"Updating Ring properties")
    
        #Update radius
        self.ri=self.fi*self.parent.radius
        self.re=self.fe*self.parent.radius
        self.radius=self.re
        
        #Update geometry args for spangling purposes
        self.geometry_args=dict(ri=self.ri/self.re)
        
    def update_ring(self,**props):
        """General and specific update properties of the `Planet`
        
        Parameters
        ----------------------
        **props: dictionary:
            Properties to update.
            The current object is updated with new values provided in this new object
    
        Attributes
        -------------------------
        ri, re: `float`
            Radius of the inner (outer) border of the ring in units of the parent radius.

        albedo_gray_normal: `float`
            Lambertian (normal) gray (wavelength indpendent) albedo of the spangle.
            It takes 0 to 1 values. 1 for total reflection. Default = 1

        tau_gray_optical: `float`
            Gray (wavelength indpendent) Optical Depth of the spangle.  
            Default = 0, i.e., the spangle is entirely transparent to all wavelength, despite its type. 
        """
        verbose(VERB_VERIFY,"Updating Ring")
        Body.update_body(self,**props)
        self._update_ring_properties()   



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Class Observer
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Observer(Body):
    """
    It initializes an Observer object with default properties defined in :any:`consts.OBSERVER_DEFAULTS`

    Note
    --------------
    This class is intended only for legacy purposes.

    Attributes
    -------------------------
    lamb, beta: `float`
        Ecliptic longitude/latitude of the observer in radians. Defaults to 0.
    """
    def __init__(self,
                 parent=None,
                 **props
                ):
        Body.__init__(self,"Observer",OBSERVER_DEFAULTS,parent,**props)
