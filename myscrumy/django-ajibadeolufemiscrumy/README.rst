====================
ajibadeolufemiscrumy
====================
ajibadeolufemiscrumy is a simple django app, details will be updated soon.

Quick start
-----------

1. Add "ajibadeolufemiscrumy" to your INSTALLED_APPS settings like this ::

        INSTALLED_APPS=[
            '---',
            'ajibadeolufemiscrumy',
        ]

2. Include the ajibadeolufemiscrumy URLconf in your project urls.py file like this ::
        
        path('ajibadeolufemiscrumy/', include('ajibadeolufemiscrumy.urls')),

3. Run `python manage.py migrate` to create the ajibadeolufemiscrumy models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (You'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ajibadeolufemiscrumy/ to participate in the poll.
