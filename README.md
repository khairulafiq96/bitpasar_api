# BitPasar API
## This is the API for bitPasar

# Description
## Main Features of the API
- To manage the account of the user/merchant
- To display the advertisements details
- To manage the advertisement, orders & purchases made by the user

# Security Concerns
- Security
> Currently, there is no OAUTH implemented in the app. Therefore, a key is required anytime the client accesses the endpoint. If the client does not contain the key, 401 unauthorized is returned
- Firebase
> No authorization were implemented in accessing the firebase storage files (Upload, Delete, Edit)

# How to run
Installing the dependencies
> pip install -r requirements.txt

Run the application
> python -m flask run

# Developed with
  - Python :  3.10.5
  - PostgresSQL 14
  - PgAdmin 4
  - Deployed to : Heroku

# Requirements

## Funtional Requirements
*** As stated in the description ***
- To manage the account of the user/merchant
- To display the advertisements details
- To manage the advertisement, orders & purchases made by the user

## Security Requirement
- CORS

# Software Development Requirements
- Python :  3.10.5
- PostgresSQL 14
- PgAdmin 4
- Deployed to : Heroku
- Access to Firebase Storage
- obtain the initializeConfig for firebase storage settings


# Table of content
- [REST API](#rest-api)
  * [Headers](#headers)
  * [Registers users with connected wallet to bitPasar](#registers-users-with-connected-wallet-to-bitpasar)
    + [Request](#request)
      - [Body](#body)
    + [Responses](#responses)
      - [Successful registration](#successful-registration)
      - [Duplicated account](#duplicated-account)
  * [Update registered user details](#update-registered-user-details)
    + [Request](#request-1)
      - [Body](#body-1)
    + [Responses](#responses-1)
      - [Successful update](#successful-update)
  * [Get user details](#get-user-details)
    + [Request](#request-2)
      - [Body](#body-2)
    + [Responses](#responses-2)
      - [Successful response](#successful-response)
      - [Unregistered user response](#unregistered-user-response)
  * [Add new advertisement](#add-new-advertisement)
    + [Request](#request-3)
      - [Body](#body-3)
    + [Responses](#responses-3)
      - [Successful response](#successful-response-1)
  * [Get all marketplace items based on the input value](#get-all-marketplace-items-based-on-the-input-value)
    + [Request](#request-4)
      - [Body](#body-4)
    + [Responses](#responses-4)
      - [Successful response](#successful-response-2)
  * [Get all marketplace items based on the input value](#get-all-marketplace-items-based-on-the-input-value-1)
    + [Request](#request-5)
      - [Body](#body-5)
    + [Responses](#responses-5)
      - [Successful response](#successful-response-3)
  * [Get all marketplace page number](#get-all-marketplace-page-number)
    + [Request](#request-6)
      - [Body](#body-6)
    + [Responses](#responses-6)
      - [Successful response](#successful-response-4)
  * [Create a new order](#create-a-new-order)
    + [Request](#request-7)
      - [Body](#body-7)
    + [Responses](#responses-7)
      - [Successful response](#successful-response-5)
  * [Get user purchases](#get-user-purchases)
    + [Request](#request-8)
      - [Body](#body-8)
    + [Responses](#responses-8)
      - [Successful response](#successful-response-6)
  * [Get user orders](#get-user-orders)
    + [Request](#request-9)
      - [Body](#body-9)
    + [Responses](#responses-9)
      - [Successful response](#successful-response-7)
  * [Update order traking number](#update-order-traking-number)
    + [Request](#request-10)
      - [Body](#body-10)
    + [Responses](#responses-10)
      - [Successful response](#successful-response-8)
      - [Unsuccessful response](#unsuccessful-response)
  * [Get user advertisements](#get-user-advertisements)
    + [Request](#request-11)
      - [Body](#body-11)
    + [Responses](#responses-11)
      - [Successful response](#successful-response-9)
  * [Delete user advertisements](#delete-user-advertisements)
    + [Request](#request-12)
      - [Body](#body-12)
    + [Responses](#responses-12)
      - [Successful response](#successful-response-10)
      - [Unsuccessful response](#unsuccessful-response-1)
  * [Delete user account and advertisement](#delete-user-account-and-advertisement)
    + [Request](#request-13)
      - [Body](#body-13)
    + [Responses](#responses-13)
      - [Successful response](#successful-response-11)
      - [Unsuccessful response](#unsuccessful-response-2)


# REST API

## Headers
*** All request must contain the appKey ***
```
{
    "appKey" : string
}
```
---

## Registers users with connected wallet to bitPasar
`POST /registeruser`

### Request

#### Body
```
{
    "name" : string,
    "email" : string,
    "phonenum" : string,
    "address1" : string,
    "address2" : string,
    "city" : string,
    "state" : string,
    "zipcode" : string,
    "walletid" : string
}
```

### Responses

#### Successful registration
```
{
    "id": {
        "name"
        "email"
        "phonenum"
        "address1"
        "address2"
        "city"
        "state"
        "zipcode"
        "walletid"
    }
}
```

#### Duplicated account
```
{
    "status" : "denied",
    "message" : "The wallet is already created an account"
}
```

---

## Update registered user details
`POST /updateUserDetails`

### Request

#### Body
```
{
    "name" : string,
    "email" : string,
    "phonenum" : string,
    "address1" : string,
    "address2" : string,
    "city" : string,
    "state" : string,
    "zipcode" : string,
    "walletid" : string
}
```

### Responses

#### Successful update
```
{
    "id": {
        "name"
        "email"
        "phonenum"
        "address1"
        "address2"
        "city"
        "state"
        "zipcode"
        "walletid"
    }
}
```

---

## Get user details
`POST /getUserDetails`

### Request

#### Body
```
{
    "walletid" : string
}
```

### Responses

#### Successful response
```
{
    "id": {
        "name"
        "email"
        "phonenum"
        "address1"
        "address2"
        "city"
        "state"
        "zipcode"
        "walletid"
    }
}
```

#### Unregistered user response
```
{
    "status" : string,
    "message" : string
}
```

---

## Add new advertisement
`POST /addItem`

### Request

#### Body
```
{
    "ownerid" : string,
    "name" string: ,
    "type" : string,
    "shortdescription" : string,
    "longdescription" : binary,
    "itemprice" : string,
    "status" : string,
    "postagename" : string,
    "postageprice" : string,
    "images" : array["string"]
}
```

### Responses

#### Successful response
```
{
    "status" : string,
    "message" : string
}
```

---

## Get all marketplace items based on the input value
`POST /getFilteredMarketplace`

### Request

#### Body
```
{
    "page" :  string,
    "search" : string
}
```

### Responses

#### Successful response
```
{
    "id": {
        "ownerid": string,
        "title": string,
        "type": string,
        "shortdescription": string,
        "itemprice":string,
        "status": string,
        "postagename": string,
        "postageprice": string,
        "images": [string],
        "longdescription": string,
        "timestamp": UTC Timestamp with timezone,
        "ownername":string,
        "walletid": string,
        "phonenum": string,
        "location": string
    }
}
```

---

## Get all marketplace items based on the input value
`POST /getItemDetail`

### Request

#### Body
```
{
    "itemId" : string
}
```

### Responses

#### Successful response
```
{
    "id": {
        "ownerid": string,
        "title": string,
        "type": string,
        "shortdescription": string,
        "itemprice":string,
        "status": string,
        "postagename": string,
        "postageprice": string,
        "images": [string],
        "longdescription": string,
        "timestamp": UTC Timestamp with timezone,
        "ownername":string,
        "walletid": string,
        "phonenum": string,
        "location": string
    }
}
```

---

## Get all marketplace page number
`POST /marketplacePageNum`

### Request

#### Body
```
{
    "search" : string
}

```

### Responses

#### Successful response
```
{
    "totalPage": [int]
}
```

---

## Create a new order
`POST /createOrder`

### Request

#### Body
```
{
    "buyername" : string, 
    "buyerwallet": string, 
    "ownername": string, 
    "ownerwallet": string, 
    "address1": string, 
    "address2": string, 
    "city": string, 
    "state": string, 
    "zipcode": string, 
    "postagename": string, 
    "postageprice": string, 
    "buyeremail": string, 
    "buyerphonenum": string, 
    "itemid": string, 
    "ownerid": string, 
    "buyerid": string, 
    "status": string
}
```

### Responses

#### Successful response
```
{
    "status" : string,
    "message" : string
}
```

---

## Get user purchases
`POST /getUserPurchases`

### Request

#### Body
```
{
    "walletid" : string
}
```

### Responses

#### Successful response
```
{
    "id": {
        "title": string,
        "shortdescription": string,
        "itemprice": string,
        "status": string,
        "images": [string],
        "timestamp": UTC Timestamp with timezone,
        "postagename": string,
        "postageprice": string,
        "trackerid": string || null,
        "ownername": string,
        "ownerphonenum": string,
        "ownerwallet": string
    }
```

---


## Get user orders
`POST /getAllOrders`

### Request

#### Body
```
{
    "ownerid" : string
}
```

### Responses

#### Successful response
```
{
    "id": {
        "title": string,
        "shortdescription": string,
        "itemprice": string,
        "status": string,
        "images": [string],
        "timestamp": UTC Timestamp with timezone,
        "postagename": string,
        "postageprice": string,
        "trackerid": string || null,
        "ownername": string,
        "ownerphonenum": string,
        "ownerwallet": string
    }
```

---

## Update order traking number
`POST /updateOrderTracker`

### Request

#### Body
```
{
    "orderid" : string ,
    "trackerid" : string
}
```

### Responses

#### Successful response
```
{"orderid" : {
                "status" : "shipped",
                "trackerid" : string
             }}
```

#### Unsuccessful response
```
{
    "status" : string ,
    "message" : string
}
```

---

## Get user advertisements
`POST /getAllAds`

### Request

#### Body
```
{
    "ownerid" : string 
}
```

### Responses

#### Successful response
```
{
    "id": {
        "ownerid": string ,
        "title": string ,
        "type": string ,
        "shortdescription": string ,
        "itemprice": string ,
        "status": string ,
        "postagename": string ,
        "postageprice": string ,
        "images": [string],
        "longdescription": string,
        "timestamp": UTC Timestamp with timezone
    }
}
```

---

## Delete user advertisements
`DELETE /deleteAds`

### Request

#### Body
```
{
    "id" : string
}
```

### Responses

#### Successful response
```
{
    "status" : string ,
    "message" : string
}
```
#### Unsuccessful response
```
{
    "status" : string ,
    "message" : string
}
```

---

## Delete user account and advertisement
`DELETE /deleteAds`

### Request

#### Body
```
{
    "userid" : string
}
```

### Responses

#### Successful response
```
{
    "status" : string ,
    "message" : string
}
```
#### Unsuccessful response
```
{
    "status" : string ,
    "message" : string
}
```

---