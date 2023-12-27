from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        #when reading requirements there will be a \n from reading each line in the requirements.txt
        #to fix the error we replace \n with blank
        requirements=[req.replace("\n", "") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='EAZ',
    author_email='eazarabi@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)