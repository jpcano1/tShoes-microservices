let ReferenceModel = require('../models/models').Reference;
    fetch = require('node-fetch');
//-------------------
// Methods
//-------------------

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

let updateInventory = (req, designerId, data) =>
{
    req.headers['content-type'] = 'application/json';
    let options = {
        method: 'PUT',
        body: JSON.stringify(data),
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
 *
 * @param req
 * @param res
 * @returns {*|Promise<any>}
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
 *
 * @param req
 * @param res
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
 *
 * @param req
 * @param res
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
 *
 * @param req
 * @param res
 */
exports.updateReference = function(req, res)
{
    if(req.body)
    {
        ReferenceModel.findOneAndUpdate(
            {
                id: req.params.id
            },
            req.body,
            {
                new: true
            })
            .then(doc =>
            {
                res.status(201).json(doc);
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};

/**
 *
 * @param req
 * @param res
 */
exports.deleteReference = function(req, res)
{
    if(req.params.id)
    {
        let id = req.params.id;
        ReferenceModel.findOneAndRemove({
            id: id
        })
            .then(doc =>
            {
                res.status(204).send();
            })
            .catch(err =>
            {
                res.json(err);
            });
    }
};
