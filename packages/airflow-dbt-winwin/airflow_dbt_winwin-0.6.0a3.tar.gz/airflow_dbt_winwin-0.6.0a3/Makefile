VERSION = 0.6.0-alpha.3

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
	@uv publish 
 
	
all: tag build publish

