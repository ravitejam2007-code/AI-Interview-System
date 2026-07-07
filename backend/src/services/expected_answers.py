EXPECTED_ANSWERS = {
    "Explain decorators in Python and their common use cases.": {
        "expected_answer": "Decorators in Python are functions that modify the behavior of another function without changing its code. They use the @ syntax and are commonly used for logging, authentication, memoization, and timing.",
        "keywords": ["decorator", "function", "@", "wrapper", "modify", "behavior", "logging", "authentication", "memoization"]
    },
    "What is the difference between a list and a tuple in Python?": {
        "expected_answer": "A list is mutable (can be changed after creation), while a tuple is immutable (cannot be changed). Lists use square brackets [], tuples use parentheses (). Tuples are faster and can be used as dictionary keys.",
        "keywords": ["list", "tuple", "mutable", "immutable", "square bracket", "parenthesis", "[]", "()", "change", "modify", "key"]
    },
    "Explain Python's memory management and garbage collection.": {
        "expected_answer": "Python uses reference counting and a cyclic garbage collector for memory management. Objects are automatically freed when their reference count drops to zero. The gc module handles circular references.",
        "keywords": ["reference count", "garbage collection", "memory", "cyclic", "gc", "refcount", "circular reference", "automatic", "deallocate"]
    },
    "What are generators and yield in Python?": {
        "expected_answer": "Generators are functions that use the yield keyword to produce a sequence of values lazily. They maintain state between calls and are memory-efficient for large datasets. Generators can be created with generator expressions.",
        "keywords": ["generator", "yield", "lazy", "state", "iteration", "memory efficient", "__next__", "StopIteration", "generator expression"]
    },
    "Explain the bias-variance tradeoff in Machine Learning.": {
        "expected_answer": "The bias-variance tradeoff is a fundamental ML concept where models with high bias underfit (too simple) and models with high variance overfit (too complex). The goal is to find the optimal balance that minimizes total error.",
        "keywords": ["bias", "variance", "tradeoff", "underfit", "overfit", "error", "balance", "complex", "simple", "generalization"]
    },
    "What is gradient descent and how does it work?": {
        "expected_answer": "Gradient descent is an optimization algorithm that iteratively moves toward the minimum of a loss function by taking steps proportional to the negative gradient. It uses learning rate to control step size and converges to local minima.",
        "keywords": ["gradient descent", "optimization", "loss function", "learning rate", "derivative", "slope", "minimum", "converge", "iterate", "step"]
    },
    "What is the difference between overfitting and underfitting, and how do you prevent them?": {
        "expected_answer": "Overfitting occurs when a model learns noise in the training data and performs poorly on new data. Underfitting occurs when a model is too simple to capture patterns. Prevention includes cross-validation, regularization, more data, and simpler models.",
        "keywords": ["overfitting", "underfitting", "noise", "generalize", "cross-validation", "regularization", "simple", "complex", "training", "test"]
    },
    "Explain how a Random Forest classifier works.": {
        "expected_answer": "Random Forest is an ensemble method that builds multiple decision trees on bootstrapped samples and random feature subsets. It aggregates predictions via majority voting (classification) or averaging (regression), reducing overfitting.",
        "keywords": ["random forest", "decision tree", "ensemble", "bootstrap", "aggregate", "voting", "average", "overfitting", "bagging", "feature subset"]
    },
    "What is Flask and why is it called a microframework?": {
        "expected_answer": "Flask is a lightweight Python web framework called a microframework because it has minimal built-in components. It provides routing, request handling, and templating while letting developers choose extensions for databases, forms, authentication, etc.",
        "keywords": ["flask", "microframework", "lightweight", "minimal", "routing", "extension", "modular", "python", "wsgi"]
    },
    "How do you handle request parameters and route variables in Flask?": {
        "expected_answer": "Route variables are defined with <variable_name> in the route decorator and passed as function arguments. Query parameters are accessed via request.args, form data via request.form, and JSON via request.json.",
        "keywords": ["route", "variable", "<>", "request.args", "request.form", "request.json", "parameter", "argument", "decorator", "query string"]
    },
    "Explain application context and request context in Flask.": {
        "expected_answer": "Flask has two contexts: application context (g, current_app) available during request handling and CLI commands, and request context (request, session) available only during requests. They are pushed and popped automatically.",
        "keywords": ["application context", "request context", "current_app", "g", "request", "session", "push", "pop", "thread local", "proxy"]
    },
    "How do you implement database migrations in Flask?": {
        "expected_answer": "Database migrations in Flask are typically handled with Flask-Migrate, which wraps Alembic. After defining models, you run 'flask db init', 'flask db migrate', and 'flask db upgrade' to apply schema changes incrementally.",
        "keywords": ["migration", "flask-migrate", "alembic", "schema", "upgrade", "downgrade", "database", "model", "flask db"]
    },
    "What is the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN?": {
        "expected_answer": "INNER JOIN returns matching rows from both tables. LEFT JOIN returns all rows from the left table and matched rows from the right (nulls where unmatched). RIGHT JOIN is the opposite. FULL OUTER JOIN returns all rows from both tables.",
        "keywords": ["inner join", "left join", "right join", "match", "null", "intersection", "table", "foreign key", "full outer join"]
    },
    "What are indexes in SQL and how do they improve query performance?": {
        "expected_answer": "Indexes in SQL are data structures (usually B-trees) that speed up data retrieval by allowing the database to locate rows without scanning the entire table. They improve SELECT performance but slow down INSERT/UPDATE/DELETE operations.",
        "keywords": ["index", "b-tree", "query", "performance", "speed", "search", "scan", "select", "insert", "data structure"]
    },
    "Explain the ACID properties of a database transaction.": {
        "expected_answer": "ACID stands for Atomicity (all or nothing), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), and Durability (committed changes persist). These guarantee reliable database transactions.",
        "keywords": ["atomicity", "consistency", "isolation", "durability", "acid", "transaction", "commit", "rollback", "concurrent", "persist"]
    },
    "What is normalization and why is it important?": {
        "expected_answer": "Normalization organizes database tables to reduce redundancy and dependency by dividing large tables into smaller related ones. It eliminates update anomalies and ensures data integrity through normal forms (1NF, 2NF, 3NF, BCNF).",
        "keywords": ["normalization", "redundancy", "dependency", "normal form", "1nf", "2nf", "3nf", "bcnf", "anomaly", "integrity"]
    },
    "What are React Hooks and why were they introduced?": {
        "expected_answer": "React Hooks are functions like useState, useEffect, and useContext that let components use state and lifecycle features without classes. They were introduced to simplify logic reuse, avoid class complexity, and improve code organization.",
        "keywords": ["hook", "usestate", "useeffect", "usecontext", "functional component", "state", "lifecycle", "class", "reuse", "side effect"]
    },
    "Explain the virtual DOM and how React renders components.": {
        "expected_answer": "The virtual DOM is an in-memory representation of the real DOM. When state changes, React creates a new virtual DOM tree, diffs it against the previous one (reconciliation), and efficiently applies only the necessary updates to the real DOM.",
        "keywords": ["virtual dom", "diff", "reconciliation", "render", "update", "in-memory", "efficient", "real dom", "patching", "component"]
    },
    "What is the difference between state and props in React?": {
        "expected_answer": "Props (short for properties) are read-only data passed from parent to child components. State is mutable data managed within a component that triggers re-rendering when changed. Props are external, state is internal.",
        "keywords": ["props", "state", "parent", "child", "read-only", "mutable", "re-render", "component", "internal", "external"]
    },
    "How do you manage global state in a React application?": {
        "expected_answer": "Global state in React can be managed with Context API for simple cases, or libraries like Redux, Zustand, or MobX for complex applications. These provide a centralized store accessible to any component without prop drilling.",
        "keywords": ["global state", "context api", "redux", "zustand", "mobx", "store", "prop drilling", "centralized", "state management"]
    },
    "What is a closure in JavaScript?": {
        "expected_answer": "A closure is a function that has access to its outer function's variables even after the outer function has returned. It's created every time a function is defined and is commonly used for data encapsulation, currying, and callback functions.",
        "keywords": ["closure", "scope", "lexical", "outer function", "variable", "encapsulation", "callback", "currying", "memory", "return"]
    },
    "Explain the difference between let, const, and var.": {
        "expected_answer": "let and const are block-scoped, while var is function-scoped. const cannot be reassigned (but objects can be mutated). let and const were introduced in ES6 and don't hoist to window scope like var does.",
        "keywords": ["let", "const", "var", "block scope", "function scope", "hoisting", "reassign", "mutable", "es6", "temporal dead zone"]
    },
    "What is the event loop in JavaScript and how does it work?": {
        "expected_answer": "The event loop is a mechanism that handles asynchronous operations in JavaScript. It continuously checks the call stack and task queues, moving callbacks from the queue to the stack when the stack is empty, enabling non-blocking I/O.",
        "keywords": ["event loop", "call stack", "callback queue", "asynchronous", "non-blocking", "microtask", "macrotask", "promise", "settimeout"]
    },
    "Explain promises and async/await syntax.": {
        "expected_answer": "Promises represent eventual completion of async operations with .then() and .catch() chaining. Async/await is syntactic sugar over promises that makes async code read like synchronous code using the async keyword and await expressions.",
        "keywords": ["promise", "async", "await", "syntactic sugar", "synchronous", "asynchronous", "then", "catch", "resolve", "reject"]
    },
    "What is the difference between a Docker image and a Docker container?": {
        "expected_answer": "A Docker image is a read-only template with instructions for creating a container. A container is a runnable instance of an image. Images are built from Dockerfiles, containers have a writable layer and can be started, stopped, and removed.",
        "keywords": ["image", "container", "read-only", "template", "instance", "dockerfile", "writable layer", "run", "build", "layer"]
    },
    "Explain Docker Compose and how it simplifies multi-container deployments.": {
        "expected_answer": "Docker Compose defines multi-container applications in a YAML file. With a single command (docker-compose up), it creates and runs all services, networks, and volumes. It simplifies environment setup, scaling, and service orchestration.",
        "keywords": ["compose", "yaml", "multi-container", "service", "docker-compose up", "network", "volume", "orchestration", "definition"]
    },
    "How do you optimize a Dockerfile for smaller image sizes?": {
        "expected_answer": "Docker images are optimized by using smaller base images (Alpine), multi-stage builds, combining RUN commands, minimizing layers, cleaning up package caches, and using .dockerignore to exclude unnecessary files.",
        "keywords": ["alpine", "multi-stage", "layer", "base image", "size", "dockerignore", "cache", "optimize", "small", "reduce"]
    },
    "What are Docker volumes and when would you use them?": {
        "expected_answer": "Docker volumes persist data generated by containers and survive container removal. They're used for databases, shared storage between containers, and when you need to preserve state across container restarts or deployments.",
        "keywords": ["volume", "persist", "data", "storage", "container", "bind mount", "database", "state", "shared", "survive"]
    },
    "What is Amazon S3 and what are its primary use cases?": {
        "expected_answer": "Amazon S3 (Simple Storage Service) is an object storage service for storing and retrieving data. Common use cases include backup and restore, static website hosting, media storage, data lakes, and application content delivery.",
        "keywords": ["s3", "object storage", "bucket", "backup", "static website", "media", "data lake", "store", "retrieve", "scalable"]
    },
    "Explain the difference between AWS EC2 and AWS Lambda (Serverless).": {
        "expected_answer": "EC2 provides virtual servers with full control over the OS and scaling, running 24/7. Lambda runs code in response to events without managing servers, scaling automatically, and charging only for execution time. EC2 is for predictable workloads, Lambda for event-driven.",
        "keywords": ["ec2", "lambda", "serverless", "virtual server", "event-driven", "scaling", "os control", "pay per execution", "provisioned", "ephemeral"]
    },
    "What is Amazon VPC and how do you secure a database within it?": {
        "expected_answer": "Amazon VPC is a virtual private cloud for launching AWS resources in an isolated network. Databases can be secured by placing them in private subnets, using security groups and NACLs, enabling encryption, and restricting access with IAM policies.",
        "keywords": ["vpc", "subnet", "private", "security group", "nacl", "encryption", "iam", "isolated", "database", "firewall"]
    },
    "What is IAM and what is the principle of least privilege?": {
        "expected_answer": "AWS IAM (Identity and Access Management) manages users, roles, and permissions. The principle of least privilege means granting only the minimum permissions needed to perform a task, reducing security risks from excessive access rights.",
        "keywords": ["iam", "identity", "access management", "least privilege", "permission", "role", "user", "policy", "security", "minimum"]
    },
    "Can you describe a technically challenging project you worked on recently and how you resolved the obstacles?": {
        "expected_answer": "A good answer describes a specific project, the technical challenge faced, steps taken to resolve it (debugging, research, collaboration), and the outcome. It demonstrates problem-solving skills and technical depth.",
        "keywords": ["project", "challenge", "resolve", "solution", "debug", "collaboration", "outcome", "technical", "architecture", "problem-solving"]
    },
    "What is your approach to writing clean, maintainable, and well-tested code?": {
        "expected_answer": "Clean code practices include following naming conventions, keeping functions small, using design patterns, writing unit tests, doing code reviews, and following the DRY and SOLID principles.",
        "keywords": ["clean", "maintainable", "test", "naming", "function", "design pattern", "unit test", "code review", "dry", "solid"]
    },
    "How do you handle collaborating with other developers and stakeholders under tight deadlines?": {
        "expected_answer": "Effective collaboration includes clear communication, using project management tools, prioritizing tasks, doing standups, being transparent about blockers, and maintaining a blameless culture focused on solutions.",
        "keywords": ["collaboration", "communication", "priority", "deadline", "standup", "blocker", "transparent", "teamwork", "agile"]
    },
    "Describe a time you had to debug a complex system issue. What tools and methods did you use?": {
        "expected_answer": "A good answer describes using debugging tools (debugger, logs, profiler), systematic isolation techniques, reproducing the issue, analyzing root cause, and implementing a fix with verification. It highlights analytical skills.",
        "keywords": ["debug", "log", "profiler", "reproduce", "root cause", "isolate", "fix", "analysis", "systematic", "tool"]
    },
    "What strategies do you use to continuously learn and integrate new programming libraries or patterns?": {
        "expected_answer": "Common strategies include reading documentation, following blogs, taking online courses, contributing to open source, building side projects, attending conferences, and experimenting in sandbox environments.",
        "keywords": ["learn", "documentation", "course", "open source", "side project", "practice", "continuous", "blog", "tutorial", "experiment"]
    }
}
