from setuptools import setup, find_packages

setup(
    name='vlm_inference',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'openai==1.78.1',
        'opencv-python==4.11.0.86',
        'pyyaml',
        'python-dotenv>=0.9.1,<0.11',
        'Pillow==9.0.1',
        # 'resources',  # Quitado porque no existe en PyPI
    ],
    include_package_data=True,
    author='Edison Bejarano',
    author_email='tu@email.com',  # opcional pero recomendable
    description='Vision language models for robotics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://gitlab.iri.upc.edu/mobile_robotics/moonshot_project/vlm/vlm_inference',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',
)
