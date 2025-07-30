from setuptools import setup, find_packages

setup(
    name='pyqmt',
    version='1.0.3',
    author='量化交易汤姆猫',
    author_email='838993637@qq.com',
    description='A wrapper library for QMT_XTQUANT trading interface.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https:quant0808.netlify.app', # Replace with your project's GitHub URL
    packages=find_packages(),
    py_modules=['pyqmt'], # Specify the single file module
    install_requires=[
        'xtquant',
        'tabulate',
        'schedule'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    python_requires='>=3.6',
)