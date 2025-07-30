from setuptools import setup, find_packages

setup(
    name='robot-kpi-metrics',
    version="1.0.0",
    description='Custom KPI report for robot framework',
    long_description='Custom html KPI report generator using robot.result api',
    classifiers=[
        'Framework :: Robot Framework',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    keywords='robotframework report kpi metrics',
    author='Your Name',
    author_email='nvluathcmut@gmail.com',
    url='https://github.com/mrlaw74/robot-kpi-metrics',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'robotframework',
        'jinja2',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'robot-kpi-metrics=robot_kpi_metrics.runner:main',
        ]
    },
)
