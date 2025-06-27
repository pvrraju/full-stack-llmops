from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:


    requirements_list:List[str] = []

    try:

        with open('requirements.txt', 'r') as file:

            lines = file.readlines()

            for line in lines:

                requirement = line.strip()

                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print('requirements.txt file not found')


    return requirements_list

print(get_requirements())

setup(
    name = 'AI-TRAVEL-PLANNER',
    version = '0.0.1',
    author = 'vijay',
    author_email = 'pvrraju9996@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements()


)