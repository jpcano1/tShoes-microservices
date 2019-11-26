let mongoose = require('mongoose');
    autoIncrement = require('mongoose-auto-increment');
    Schema = mongoose.Schema;

const username = process.env.MONGO_USER;
const password = process.env.MONGO_PASSWORD;
const host = process.env.MONGO_HOST;
const uri = `mongodb+srv://${username}:${password}@${host}/test?retryWrites=true&w=majority`;

/**
 * Connection to mongo atlas db
 */
var connection = mongoose.createConnection(uri, {
    useNewUrlParser: true
});

/**
 * Initialize the auto-increment module
 */
autoIncrement.initialize(connection);

/**
 * Create the schema for the references
 * @type {mongoose.Schema}
 */
let ReferenceSchema = new Schema({
    // Completar Schema de Mongo
    referenceName: {
        type: String,
        required: true
    },
    description: String,
    price: {
        type: Number,
        required: true
    },
    inventory: {
        type: Number,
        required: true
    },
    stock: {
        type: Number,
        required: true
    }
});

/**
 * Add the auto-increment module
 */
ReferenceSchema.plugin(autoIncrement.plugin,
    {
        model: 'Reference',
        field: 'id',
        startAt: 1,
        incrementBy: 1
    });


module.exports = {
    Reference: connection.model('Reference', ReferenceSchema)
};
