let ReferenceModel = require('../models/models').Reference;
    fetch = require('node-fetch');
//-------------------
// Methods
//-------------------

/**
 * Obtains the inventory of the designer
 * @param request the request object
 * @param designerId the id of the designer
 */
let getInventory = (request, designerId) =>
{
    delete request.headers['content-type'];
    let options = {
        headers: request.headers
    };

    return fetch(process.env.USERS_URL + designerId + '/inventory', options)
        .then(res => res.json())
        .then(body => {
            return body;
        })
        .catch(err =>
        {
            console.log("Error", err);
        });
};

/**
 * Inserts a reference in the inventory
 * @param req the request object
 * @param designerId designer's id
 * @param data reference data
 */
let updateInventory = (req, designerId, data) =>
{
    let reference = {
        _id: data._id,
        referenceName: data.referenceName,
        price: data.price,
        id: data.id
    };

    req.headers['content-type'] = 'application/json';
    let options = {
        method: 'PUT',
        body: JSON.stringify(reference),
        headers: req.headers,
    };

    return fetch(process.env.USERS_URL + designerId + '/inventory', options)
        .then(res => res.json())
        .then(body =>
        {
            return body;
        })
        .catch(err =>
        {
            console.log(err);
        })
};

/**
 * Creates a references in the database
 * and updates the inventory
 * @param req The request object
 * @param res the response object
 */
exports.postReference = async function(req, res)
{
    let inventory = await getInventory(req, req.params.designer);

    if(inventory.designer)
    {
        req.body.inventory = {
            "_id": inventory._id,
            "designer": inventory.designer,
            "__v": inventory.__v
        };
        let model = new ReferenceModel(req.body);
        model.save()
            .then(doc =>
            {
                if(!doc || doc.length === 0)
                {
                    return res.status(404).json(doc);
                }
                updateInventory(req, req.params.designer, doc);
                return res.status(201).json(doc);
            })
            .catch(err =>
            {
                console.log(err);
                return res.status(400).json(err);
            });
    }
    else
    {
        console.log(inventory);
        await res.status(401).json(inventory);
    }
};

/**
 * Gets all the references in the database
 * @param req the request object
 * @param res the response object
 */
exports.getReferences = (req, res) =>
{
    if(req.query.id)
    {
        ReferenceModel.findOne({
            id: req.query.id
        })
            .then(doc =>
            {
                res.status(200).json(doc);
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
    else
    {
        ReferenceModel.find({})
            .then(doc =>
            {
                return res.status(200).json(doc);
            })
            .catch(err =>
            {
                return res.json(err);
            });
    }
};

/**
 * Gets a reference by its id
 * @param req the request object
 * @param res the response object
 */
exports.getReferenceById = function(req, res)
{
    if(req.params.id)
    {
        let id = req.params.id;
        ReferenceModel.findOne({
            id: id
        })
            .then(doc =>
            {
                if(doc)
                {
                    res.json(doc);
                }
                else
                {
                    res.status(404).send();
                }
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};

/**
 * Updates the stock of a reference
 * @param req the request object
 * @param res the response object
 * @returns {Promise<void>}
 */
exports.updateReferenceStock = async (req, res) =>
{
    const query = ReferenceModel.findOne({ id: req.params.id });
    const doc = await query;

    if(doc)
    {
        doc.stock = req.body.stock;
        doc.save()
            .then(async doc =>
            {
                if(!doc || doc.length === 0)
                {
                    return res.status(400).json(doc);
                }
                return res.status(201).json(doc);
            })
            .catch(err =>
            {
                console.log(err);
                res.status(400).json(err);
            });
    }
    else if(!doc || doc.length === 0)
    {
        res.status(404).send();
    }
};
