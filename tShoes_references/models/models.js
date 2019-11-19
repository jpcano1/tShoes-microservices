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
        type: Schema.Types.ObjectId,
        ref: 'Inventory'
    },
    stock: {
        type: Number,
        required: true
    }
});

/**
 * Create the schema for the inventory
 * @type {mongoose.Schema}
 */
let InventorySchema = new Schema({
    // Completar Schema de mongo
    designerId: Number,
    references: [ReferenceSchema]
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

/**
 * Add the auto-increment module
 */
InventorySchema.plugin(autoIncrement.plugin,
    {
        model: 'Inventory',
        field: 'id',
        startAt: 1,
        incrementBy: 1
    });

module.exports = connection.model('Reference', ReferenceSchema);
module.exports = connection.model('Inventory', InventorySchema);



