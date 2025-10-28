"""
Setup configuration for AI Resume & LinkedIn Analyzer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Development requirements
dev_requirements = [
    'pytest>=8.0.0',
    'pytest-cov>=4.1.0',
    'pytest-asyncio>=0.23.3',
    'pytest-mock>=3.12.0',
    'black>=24.1.1',
    'isort>=5.13.2',
    'flake8>=7.0.0',
    'pylint>=3.0.3',
    'mypy>=1.8.0',
    'pre-commit>=3.6.0',
    'faker>=22.6.0',
]

setup(
    name='ai-resume-linkedin-analyzer',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='AI-powered resume analysis and LinkedIn job matching platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ai-resume-linkedin-analyzer',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/ai-resume-linkedin-analyzer/issues',
        'Source': 'https://github.com/yourusername/ai-resume-linkedin-analyzer',
        'Documentation': 'https://github.com/yourusername/ai-resume-linkedin-analyzer/docs',
    },
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'scripts']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='resume analyzer, job matching, ai, nlp, linkedin scraper, career',
    python_requires='>=3.9',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'test': [
            'pytest>=8.0.0',
            'pytest-cov>=4.1.0',
            'pytest-asyncio>=0.23.3',
        ],
    },
    entry_points={
        'console_scripts': [
            'resume-analyzer=app.main:main',
            'init-db=scripts.init_db:main',
            'seed-data=scripts.seed_data:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.yaml', '*.yml', '*.json'],
        'config': ['*.yaml', '*.yml'],
    },
    zip_safe=False,
)