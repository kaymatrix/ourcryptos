cd G:\pythonworkspace\ourcryptos\build\gcloudfn
g:
rmdir G:\pythonworkspace\ourcryptos\build\gcloudfn\lib /s /q
xcopy G:\pythonworkspace\ourcryptos\lib G:\pythonworkspace\ourcryptos\build\gcloudfn\lib /e/f/c/i/y
copy G:\pythonworkspace\ourcryptos\requirements.txt G:\pythonworkspace\ourcryptos\build\gcloudfn\requirements.txt /y
rmdir G:\pythonworkspace\ourcryptos\build\gcloudfn\lib\unittest /s /q
rmdir G:\pythonworkspace\ourcryptos\build\gcloudfn\lib\__pycache__ /s /q
rmdir G:\pythonworkspace\ourcryptos\build\gcloudfn\lib\cryptlibs\__pycache__ /s /q
del /s /q *.pyc
del /s /q __pycache__
del /s /q *cdatastore
del /s /q *ctracker
del /s /q unittest
del /s /q *_slug
del /s /q GCP_DATA_LIB.py
del /s /q unittest\*.*
del /s /q gcp.zip
d:\7-Zip\7z a gcp.zip * -xr!unittest\*.* 
rmdir G:\pythonworkspace\ourcryptos\data\last_gcp_build /s /q
xcopy G:\pythonworkspace\ourcryptos\build\ G:\pythonworkspace\ourcryptos\data\last_gcp_build /e/f/c/i/y
pause