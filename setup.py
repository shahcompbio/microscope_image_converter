from setuptools import setup, find_packages
import versioneer


setup(
    name='microscope_image_converter',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Microscope image converter',
    author='Andrew McPherson',
    author_email='andrew.mcpherson@gmail.com',
    entry_points={'console_scripts': ['microscope_image_converter = microscope_image_converter.run:main']},
    package_data={},
)
