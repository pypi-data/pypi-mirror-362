## Version

- Python 3.12.3

## Limpiar

``` shell
Remove-Item -Recurse -Force build, dist, ecom_statics.egg-info
```

## Actualizar

``` shell
python setup.py sdist bdist_wheel
```

## Publicar en Produccion

``` shell
twine upload dist/*
```

## Instalar

``` shell
pip install ecom-statics
```
