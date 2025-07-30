from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-admin-query-executor",
    version="1.0.0",
    author="Jeff Turner",
    author_email="jeff@torusoft.com",
    description="Execute Django ORM queries directly from the admin interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j4rf/django-admin-query-executor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    include_package_data=True,
    package_data={
        "django_admin_query_executor": [
            "static/admin/css/*.css",
            "static/admin/js/*.js",
            "templates/admin/*.html",
            "templates/admin/**/*.html",
        ],
    },
    keywords="django admin query executor orm database",
    project_urls={
        "Bug Reports": "https://github.com/j4rf/django-admin-query-executor/issues",
        "Source": "https://github.com/j4rf/django-admin-query-executor",
        "Documentation": "https://github.com/j4rf/django-admin-query-executor/blob/main/README.md",
    },
)
