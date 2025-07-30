The idea is simple : in one file (like an env.py), you define your constants, with the same name as your env variables and you give them a type. At the end of this file, you call the loader (as you would do with python-dotenv for example).


After that, all the constants in the env.py file are loaded, and you can import them from other modules, with your IDE knowing they exist, and what their type is.