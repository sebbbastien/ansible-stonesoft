############
Fact Modules
############   

Fact modules all provide the same interface for retrieving high level or detailed information about specified elements and their existence.

Fact modules are separated by functional area in an attempt to keep the design flexible and modular. 

Searching the SMC using these modules uses the smc-python `Collections Interface <http://smc-python.readthedocs.io/en/latest/pages/collections.html>`_. The format of a search query is determined by the element searched as well as filters that are used. It is also possible to specify case sensitivity, exact match, as well as limit the number of results.

Face module arguments will have the same (or very close) signature:

.. code::

  "module_args": {
            "case_sensitive": true, 
            "element": "engine_clusters", 
            "exact_match": false, 
            "filter": null, 
            "limit": 0, 
            "smc_address": null, 
            "smc_alt_filepath": null, 
            "smc_api_key": null, 
            "smc_api_version": null, 
            "smc_domain": null, 
            "smc_extra_args": null, 
            "smc_timeout": 30
  }

Where:

**element**: Defines the element type to search. Each module will have choices based on the module and function.

**filter**: Defines an optional filter to apply to the search. Filters provide the ability to do `contains` searching when finding elements. Most searches will also match the comment field and the element's main key. If a search is made for hosts using a filter of '1.1.1.1', hosts with this address assigned would be returned, even though there may not be a host with '1.1.1.1' in it's name.

**case_sensitive**: Turn off case sensitivity for the search. By default, case sensitivity is turned on.

**exact_match**: Defines that there must be an exact match in order for the match to succeed. If a host were named 'myhost' and the search filter was 'myho', this would not constitute a match. 

**limit**: Limit the number of results to return

**as_yaml**: Return the data in yaml format. Use a jinja template from the templates directory to format the yaml into a file of choice

Some modules may also support the **expand** option which can be used to expand attributes that are returned and only have an href
as value. Each fact module that supports expand also has a list of supported attributes that can be expanded.

.. note:: Best effort is made to keep this interface consistent for all fact 
  modules, however it is advised to check the module documentation to verify additional settings that may be supported.

Let's start with some simple search examples.

Using the network_element facts module to find all hosts:

Playbook example:

.. code::

  - name: find all hosts
    network_element_facts:
      element: host

Only the `element` variable was specified (no filter). This is a generic search that will return all elements of type host. 

.. code::

  "elements": [
      {
      "name": "DHCP Broadcast Destination", 
      "type": "host"
      }, 
      {
      "name": "kali", 
      "type": "host"
      }
      ...

The metadata returned will provide insight into the element type and name, allowing for more specific searching. This return format is identical for all generic searches.

To further refine a search, add a filter to either specify the host entry you are interested in retrieving, or if the name is unknown, a partial filter name:

.. code:

  - name: find only a specific host
    network_element_facts:
      element: host
      filter: kali

Using a filter will return the specific drill down data for any matches found, for example:

.. code::

  "elements": [
      {
      "address": "2.2.2.2", 
      "comment": null, 
      "ipv6_address": null, 
      "name": "kali", 
      "secondary": [
          "23.23.23.25"
      ], 
      "type": "host"
      }
  ]

Notice that in this filter the elements `name` was specified. There may be cases where you don't have the name and instead want all entries with a given value. For example, show me all hosts with an IP address of '1.1.1.1':

We can just switch the filter to the specific IP address we are looking for to get those results:

.. code::

  - name: add a layer 3 interface to a single fw
    network_element_facts:
      element: host
      filter: 1.1.1.1

Example output:

.. code::

  "elements": [
      {
      "address": "1.1.1.1", 
      "comment": null, 
      "ipv6_address": null, 
      "name": "someotherhost", 
      "secondary": [
          "1.1.1.2"
      ], 
      "type": "host"
      }, 
      {
      "address": "1.1.1.1", 
      "comment": null, 
      "ipv6_address": null, 
      "name": "foohost", 
      "secondary": [], 
      "type": "host"
      }
  ]

An example of retrieving a group and using the `expand` attribute to display all of the group members:

.. code::

  - name: Retrieve a specific group and expand all members
    network_element_facts:
      element: group
      filter: foogroup
      expand:
        - group
        
And the results which show expanded group members:

.. code::

  "elements": [
    {
        "comment": null, 
        "members": [
		{
	        "comment": null, 
	        "ipv4_network": "6.6.6.0/24", 
	        "ipv6_network": null, 
	        "name": "another_net", 
	        "type": "network"
	        }, 
	        {
	        "comment": null, 
	        "name": "domain.com", 
	        "type": "domain_name"
	        }, 
	        {
	        "comment": null, 
	        "ipv4_network": "12.12.12.0/24", 
	        "ipv6_network": null, 
	        "name": "anothernet", 
	        "type": "network"
		}], 
    	"name": "foogroup", 
    	"type": "group"
    }
  ]
  
        
The same methodology applies to other network elements as well.

To view common attributes of network elements, see: `Elements <http://smc-python.readthedocs.io/en/latest/pages/reference.html#elements>`_.

Below is a list of fact modules currently provided for ansible-stonesoft:

.. toctree::
   :glob:
   
   *
  
