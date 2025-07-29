from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

with open("requirements.txt", "r") as arq:
    requirements = arq.read().splitlines()

setup(name='tes_thermo',
    version='0.0.1',
    license='MIT License',
    author='Julles Mitoura, Antonio Freitas and Adriano Mariano',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mitoura96@outlook.com',
    keywords='ming, thermodynamic, virial, reactions',
    description=u'TeS is a tool for simulating reaction processes. It uses the Gibbs energy minimization approach with the help of Pyomo and Ipopt as solvers.',
    packages=['tes_thermo'],
    install_requires=requirements,)