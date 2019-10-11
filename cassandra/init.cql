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
    author text, title text, content text, PRIMARY KEY(author, title)
);

-- ----------------------------------------------------------------- --
--  POSTS                                                            --
-- ----------------------------------------------------------------- --
INSERT INTO posts(author, title, content) VALUES ('anthony', 'Post 01', 'Content 01');
