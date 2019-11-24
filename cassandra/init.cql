-- 
-- @author      Anthony Vilarim Caliani
-- @contact     github.com/avcaliani
-- 
-- @description
-- Mr. Owlf database initialization script
-- 

-- ----------------------------------------------------------------- --
--  KEYSPACE                                                         --
-- ----------------------------------------------------------------- --
create keyspace mr_owlf_ks with replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE mr_owlf_ks;

-- ----------------------------------------------------------------- --
--  TBL POSTS                                                        --
-- ----------------------------------------------------------------- --
CREATE TABLE posts (
    author text, title text, last_update timestamp, domain text, classification text, PRIMARY KEY(author, title, last_update)
);

