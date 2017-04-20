Rapnet API
==========

This is a very primary API SDK to work with Rapnet_.

----

Currently it only supports `Premium JSON API`_ and Price List API.


=====
Usage
=====
Simply Instantiate a ``RapNetAPI`` object with proper ``usernmae`` and ``password``.

.. code:: python

   from rapnet import RapNetAPI
   rapi = RapNetAPI()


Functions
---------

**get_price_sheet_info**
  *Arguments: None*
  Returns price sheet's metadata.

**get_price_sheet**
  *Arguments: Shape[Optional]*
  Returns price list sheet by shape.

**get_price_changes**
  *Arguments: Shape[Optional]*
  Returns price changes by shape.

**get_price**
  *Arguments: params(format: JSON)[Optional]*
  Returns filtered price list. For filters consult `Price Doc`_.

**get_diamonds_list**
  *Arguments: params(format: JSON)[Optional]*
  Returns paginated, filtered diamond details. For filter parameters consult `Details Doc`_.

**get_diamond**
  *Arguments: id(format: Integer)*
  Return a single diamond detail by ID.

**get_all_diamonds**
  *Arguments: datafile(format: String)[Optional]*
  Return all diamonds details in the API. Time Consuming, Beware!

.. _Rapnet: https://technet.rapaport.com
.. _`Premium JSON API`: https://technet.rapaport.com/Info/RapLink/Format_Json.aspx
.. _`Price Doc`: https://technet.rapaport.com/Info/Prices/Format_Json.aspx
.. _`Details Doc`: https://technet.rapaport.com/Info/RapLink/Format_Json.aspx
