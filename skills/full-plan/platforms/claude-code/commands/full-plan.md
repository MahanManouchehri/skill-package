---
description: Create the complete API endpoint plan and ordered user scenarios before implementation.
---

Create «طرح API و سناریوها» for the current request before changing any code.

Inspect only the relevant project evidence: routes, handlers or services, validation, serializers, authorization, responses, and API documentation. Clearly distinguish existing endpoints, proposed endpoints, and decisions that require user input. Do not invent routes, fields, status codes, or response contracts.

For every required endpoint, provide:

1. A readable name, HTTP method, exact path, current/proposed status, and required access.
2. All path, query, body, and header inputs with type, required status, example, validation, and purpose.
3. A concise description of authorization, validation, primary behavior, and observable result.
4. An exact successful JSON response and status code; explain every response field and each expected error.

Then write ordered, role-based scenarios. For every step, name the actor, purpose, endpoint, important input/output passed to the next step, and observable result.

Write all explanatory prose in natural, professional Persian. Preserve route names and JSON keys exactly. End with existing/proposed/open decisions and ask the user for explicit confirmation. Do not implement code, alter an API contract, run migrations, or make other execution changes until that confirmation is received.
