======================
T-Vault
======================

Package for seamless interaction with the Bitwarden and others Password Managers.

--------------

Installation
------------

.. code:: bash

   pip install t-vault-manager

--------------

Usage
-----

Login to Bitwarden
------------------

.. code:: python

   from t_vault import bw_login, bw_login_from_env
   from RPA.Robocorp.Vault import Vault

   if Config.LOCAL_RUN:
       bw_login_from_env()
   else:
       bw_login(**Vault().get_secret("bitwarden_credentials"))

To use ``bw_login_from_env()`` you need the following environment
variables set:

-  ``BW_PASSWORD``
-  ``BW_CLIENTID``
-  ``BW_CLIENTSECRET``

To use if you do not have those env vars set, you can use ``bw_login``:

.. code:: python

   bw_login(client_id, client_secret, password, username)

Getting Vault Items:
--------------------

There is no need of adding ``CREDENTIALS`` variable to ``config.py``
anymore.

You can get the a Vault Item like this:

.. code:: python

   from t_vault import bw_get_item

   vault_item = bw_get_item(item_name)

The method will return a `T -
Object <https://www.notion.so/T-Object-1900a37f5cb74a1e9ca5158e5957e4e2?pvs=21>`__
with the vault item data. 


Getting Attachments
-------------------

There is two ways to get an attachment:

.. code:: python

   downloaded_path = bw_get_item(item_name).get_attachment(attachment_name, file_path)

.. code:: python

   downloaded_path = bw_get_attachment(item_name, attachment_name, file_path)

in both methods, ``file_path`` is optional. If it is not set, it will
download to the ``cwd`` .

Updating passwords
------------------

There is two ways to reset a password with the lib:

.. code:: python

   from t_vault import bw_update_password

   new_password = bw_update_password(item_name, new_password)

.. code:: python

   from t_vault import bw_get_item
   new_password = bw_get_item(item_name).update_password(new_passord)

The ``new_password`` argument is optional, and if is not passed, the
library will generate a strong password for you.

Those methods returns the newly created password.

===============
Troubleshooting
===============

If you are getting the following error:
``Failed to login: You are already logged in as...`` it is probably a
problem with the CLI executable. A potential fix to this is to force the
library to download the latest version of the CLI (currently, by
default, the library will use a stable version of the executable). To do
this you can add the ``force_latest=True`` argument to the login
methods:

.. code:: python

   bw_login(client_id="...", client_secret="...", password="...", force_latest=True)

or

.. code:: python

   bw_login_from_env(force_latest=True)

=====================================
Replacing old credentials dictionary:
=====================================

Use this if you just want to replace the old credentials dictionary that
is in most AIAs:

.. code:: python

   from t_vault import bw_login, bw_get_item

   bw_login(**Vault().get_secret("bitwarden_credentials"))
   credentials = {k: bw_get_item(v).to_dict() for k, v in collection.items()}
