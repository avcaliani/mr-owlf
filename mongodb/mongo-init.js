/*
 * @author      avcaliani
 * @project     mr-owlf
 * @description Initialization Script
 */

db.createUser({
    user: "root",
    pwd: "root",
    roles: [ { role: "dbOwner", db: "mr-owlf-db" } ]
});

db.createUser({
    user: "dss",
    pwd: "D4t4SS",
    roles: [
        { role: "readWrite", db: "mr-owlf-db" }
    ]
});

