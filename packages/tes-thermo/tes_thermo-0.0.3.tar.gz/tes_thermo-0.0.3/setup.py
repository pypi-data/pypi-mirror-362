from setuptools import setup

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name='tes_thermo',
    version='0.0.3',
    license='MIT License',
    author='Julles Mitoura, Antonio Freitas and Adriano Mariano',
    author_email='mitoura96@outlook.com',
    description='TeS is a tool for simulating reaction processes. It uses the Gibbs energy minimization approach with the help of Pyomo and Ipopt as solvers.',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='gibbs, thermodynamics, virial, reactions, simulation, pyomo',
    packages=['tes_thermo'],
    install_requires=[
        'pandas==2.3.1',
        'numpy==2.3.1',
        'scipy==1.16.0',
        'pyomo==6.9.2',
    ],
)