# Stock API

This API provides a basic wrapper around the [Markit On Demand](https://www.markit.com/product/markit-on-demand) stock API. That API uses XML, which I have converted into a JSON API to simplify integrations.

## Quote Symbol Lookup

This endpoint allows a consumer to lookup a company's quote symbol with a partial symbol or partial company name.
| Field         | Type           | Description  |
| ------------- |:-------------:| -----:|
| input      | string | Partial symbol or partial company name |

## Quote Lookup

This endpoint gives the consumer information about the given quote symbol
| Field         | Type           | Description  |
| ------------- |:-------------:| -----:|
| symbol      | string | valid quote symbol |