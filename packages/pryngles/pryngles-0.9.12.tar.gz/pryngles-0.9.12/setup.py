##################################################################
#                                                                #
# #####...#####...##..##..##..##...####...##......######...####..#
# ##..##..##..##...####...###.##..##......##......##......##.....#
# #####...#####.....##....##.###..##.###..##......####.....####..#
# ##......##..##....##....##..##..##..##..##......##..........##.#
# ##......##..##....##....##..##...####...######..######...####..#
# ...............................................................#
#                                                                #
# PlanetaRY spanGLES                                             #
#                                                                #
##################################################################
# License http://github.com/seap-udea/pryngles-public            #
##################################################################
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # ######################################################################
    # BASIC DESCRIPTION
    # ######################################################################
    name='pryngles',
    author="Jorge I. Zuluaga, Allard Veenstra, Sebastian Numpaque, Mario Sucerquia and Jaime A. Alvarado-Montes",
    author_email="jorge.zuluaga@udea.edu.co",
    description="PlanetaRY spanGLES: general photometry of planets, rings and shadows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pryngles",
    keywords='astronomy exoplanets planetary-rings',
    license='MIT',

    # ######################################################################
    # CLASSIFIER
    # ######################################################################
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    version='0.9.12',

    # ######################################################################
    # FILES
    # ######################################################################
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    
    # ######################################################################
    # EXTENSIONS
    # ######################################################################
    ext_modules=[
        setuptools.Extension(name="pryngles.cpixx",
                  sources=["src/pryngles/cpixx/cpixx.c",
                           ]),
    ],
    
    # ######################################################################
    # ENTRY POINTS
    # ######################################################################
    entry_points={
        'console_scripts': ['install=pryngles.install:main'],
    },

    # ######################################################################
    # TESTS
    # ######################################################################
    test_suite='nose.collector',
    tests_require=['nose'],

    # ######################################################################
    # DEPENDENCIES
    # ######################################################################
    install_requires=['rebound','scipy','ipython',
	              'matplotlib','tqdm','dill',
	              'spiceypy','cmasher','pandas','celluloid',
	              'sigfig','anytree','ipywidgets','gdown'],

    # ######################################################################
    # OPTIONS
    # ######################################################################
    include_package_data=True,
    package_data={"": ["data/*.*", "data/sampler_presets/*.*", "tests/*.*"]},
)
