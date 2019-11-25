let ReferenceModel = require('../models/models').Reference;
    request = require('request');
//-------------------
// Methods
//-------------------

/**
 *
 * @param req
 * @param res
 * @returns {*|Promise<any>}
 */
exports.postReference = async function(req, res)
{
    let data = {};

    fetch("url")
    .then((response) =>
    {
        
    })
    .then((jsonData) =>
    {
        return jsonData;
    });

    res.send("Hola");
    // if(!req.body)
    // {
    //     return res.status(401).json({
    //         message: "Request body is missing"
    //     });
    // }
    // let data = req.body;
    // data.inventory = algo.id;
    //
    // let model = new ReferenceModel(data);
    // model.save()
    //     .then(doc =>
    //     {
    //         if(!doc || doc.length === 0)
    //         {
    //             return res.status(500).json(doc);
    //         }
    //         return res.status(201).json(doc);
    //     })
    //     .catch(err =>
    //     {
    //         return res.status(500).json(err);
    //     });
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
                res.status(200).json(doc);
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
