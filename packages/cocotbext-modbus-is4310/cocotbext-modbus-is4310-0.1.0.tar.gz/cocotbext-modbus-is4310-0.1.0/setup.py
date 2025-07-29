from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='cocotbext-modbus-is4310',
    version='0.1.0',
    description='Reusable Verification IP for MODBUS RTU Protocol (IS4310-based) using Cocotb',
    #long_description=long_description,
    #long_description_content_type='text/markdown',
    author='Rohith Mudigonda',
    author_email='rohith.mudigonda@example.com',
    url='https://github.com/RohithVeer/cocotbext-modbus-rtu',
    packages=find_packages(include=['cocotbext', 'cocotbext.modbus']),
    install_requires=[
        'cocotb>=1.7',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
)

