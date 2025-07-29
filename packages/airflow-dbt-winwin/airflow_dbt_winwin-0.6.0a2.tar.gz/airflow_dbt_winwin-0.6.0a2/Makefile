VERSION = 0.6.0-alpha.2

version:
	echo "version = '$(VERSION)'" > airflow_dbt/__version__.py
	 
tag:
	echo "version = '$(VERSION)'" > airflow_dbt/__version__.py
	git add -u  
	git commit -m "tag: v$(VERSION)"
	git tag v$(VERSION)
	git push --tags

build:
	uv build


publish:	
	@uv publish --token $(PYPI_TOKEN)
 
	
all: tag build publish

