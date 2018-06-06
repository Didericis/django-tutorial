# Objectives

Figure out a good way to organize api routes

## References
- https://stackoverflow.com/questions/31483282/django-rest-framework-combining-routers-from-different-apps

#### Option 1
```
/api/polls/choices
/api/polls/questions
/api/snippets/snippets
/api/users
```

**Pros**

- Namespacing prevents resource name collisions between apps
- Having all api routes under `/api` looks nice

**Cons**

- Cannot declare all routes for each app in one place
- `snippets/snippets` is a bit ugly

#### Option 2
```
/polls/api/choices
/polls/api/questions
/snippets/api/snippets
/api/users
```

**Pros**
- Each app can declare it's routes in one place
- Namespacing prevents resource name collisions between apps

**Cons**
- Encourages api prefixes with different names
- Probably puts too much emphasis on app separation

#### Option 3 (chosen)
```
/api/choices
/api/questions
/api/snippets
/api/users
```

**Pros**
- Avoids emphasis on app name
- Having all api routes under `/api` looks nice

**Cons**
- Could be resource name collisions between apps

