/*
 * @author      Anthony Vilarim Caliani
 * @contact      github.com/avcaliani
 *
 * @description
 * Mr. Owlf database initialization script
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

db.createUser({
    user: "mls",
    pwd: "ML34rn",
    roles: [
        { role: "read", db: "mr-owlf-db" }
    ]
});

db.createUser({
    user: "api",
    pwd: "4P1",
    roles: [
        { role: "read", db: "mr-owlf-db" }
    ]
});
