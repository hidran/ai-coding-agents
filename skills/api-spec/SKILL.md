---
name: api-spec
description: Generates OpenAPI 3.1 specifications from natural language descriptions. Outputs YAML with paths, schemas, authentication, and examples.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# OpenAPI Spec Generator

This skill generates a complete OpenAPI 3.1 specification from a natural language description of an API.

## Usage

Run `/api-spec <ResourceName>` or `/api-spec <description>`

## Structure

Generates:
- `docs/api/<resource-name>.openapi.yaml`: Full OpenAPI 3.1 spec
- `docs/api/schemas/<resource-name>.yaml`: Reusable schema components (if complex)

## Standards

- **OpenAPI 3.1**: Always use the latest spec version
- **RESTful conventions**: Proper HTTP methods, status codes, resource naming
- **Schemas**: Use JSON Schema with examples, required fields, formats
- **Authentication**: Include security schemes (Bearer JWT, API Key, OAuth2)
- **Pagination**: Include cursor-based or offset pagination patterns
- **Error responses**: Standard error format (RFC 7807 Problem Details)
- **Versioning**: URL path versioning (/v1/)
- **Examples**: Include request/response examples for every endpoint

## Process

1. Read existing API specs in the project (if any) to match conventions
2. Ask for the resource name and key attributes if not provided
3. Generate CRUD endpoints + common operations
4. Include proper schemas with validation constraints
5. Add authentication and error responses

## Example

Below is a complete OpenAPI 3.1 YAML specification for a "Product" resource. Use this as a reference template when generating specs.

```yaml
openapi: 3.1.0
info:
  title: Product API
  description: |
    API for managing products in the catalog. Supports full CRUD operations
    with pagination, filtering, and standard error handling.
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com
    description: Production
  - url: https://staging-api.example.com
    description: Staging
  - url: http://localhost:3000
    description: Local development

security:
  - bearerAuth: []

tags:
  - name: Products
    description: Product catalog management

paths:
  /v1/products:
    get:
      operationId: listProducts
      summary: List products
      description: Returns a paginated list of products. Supports filtering by status and category.
      tags:
        - Products
      parameters:
        - name: page
          in: query
          description: Page number (1-based)
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
          example: 1
        - name: per_page
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
          example: 20
        - name: status
          in: query
          description: Filter by product status
          required: false
          schema:
            type: string
            enum:
              - active
              - draft
              - archived
          example: active
        - name: category
          in: query
          description: Filter by category slug
          required: false
          schema:
            type: string
          example: electronics
        - name: sort
          in: query
          description: Sort field and direction
          required: false
          schema:
            type: string
            enum:
              - created_at
              - -created_at
              - price
              - -price
              - name
              - -name
            default: -created_at
          example: -created_at
      responses:
        "200":
          description: A paginated list of products
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PaginatedProductResponse"
              example:
                data:
                  - id: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"
                    name: "Wireless Bluetooth Headphones"
                    slug: "wireless-bluetooth-headphones"
                    description: "Premium noise-cancelling wireless headphones with 30-hour battery life."
                    price: 79.99
                    currency: "USD"
                    status: "active"
                    category: "electronics"
                    sku: "WBH-001"
                    inventory_count: 150
                    tags:
                      - audio
                      - wireless
                    created_at: "2025-09-15T10:30:00Z"
                    updated_at: "2025-09-20T14:00:00Z"
                pagination:
                  page: 1
                  per_page: 20
                  total: 85
                  total_pages: 5
                  has_next: true
                  has_prev: false
        "401":
          $ref: "#/components/responses/Unauthorized"
        "500":
          $ref: "#/components/responses/InternalServerError"

    post:
      operationId: createProduct
      summary: Create a product
      description: Creates a new product in the catalog.
      tags:
        - Products
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductCreate"
            example:
              name: "Wireless Bluetooth Headphones"
              description: "Premium noise-cancelling wireless headphones with 30-hour battery life."
              price: 79.99
              currency: "USD"
              status: "draft"
              category: "electronics"
              sku: "WBH-001"
              inventory_count: 150
              tags:
                - audio
                - wireless
      responses:
        "201":
          description: Product created successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
              example:
                id: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"
                name: "Wireless Bluetooth Headphones"
                slug: "wireless-bluetooth-headphones"
                description: "Premium noise-cancelling wireless headphones with 30-hour battery life."
                price: 79.99
                currency: "USD"
                status: "draft"
                category: "electronics"
                sku: "WBH-001"
                inventory_count: 150
                tags:
                  - audio
                  - wireless
                created_at: "2025-09-15T10:30:00Z"
                updated_at: "2025-09-15T10:30:00Z"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "409":
          description: Product with this SKU already exists
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                type: "https://api.example.com/errors/conflict"
                title: "Conflict"
                status: 409
                detail: "A product with SKU 'WBH-001' already exists."
                instance: "/v1/products"
        "500":
          $ref: "#/components/responses/InternalServerError"

  /v1/products/{id}:
    parameters:
      - name: id
        in: path
        required: true
        description: Unique product identifier
        schema:
          type: string
        example: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"

    get:
      operationId: getProduct
      summary: Get a product
      description: Returns a single product by ID.
      tags:
        - Products
      responses:
        "200":
          description: Product details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
              example:
                id: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"
                name: "Wireless Bluetooth Headphones"
                slug: "wireless-bluetooth-headphones"
                description: "Premium noise-cancelling wireless headphones with 30-hour battery life."
                price: 79.99
                currency: "USD"
                status: "active"
                category: "electronics"
                sku: "WBH-001"
                inventory_count: 150
                tags:
                  - audio
                  - wireless
                created_at: "2025-09-15T10:30:00Z"
                updated_at: "2025-09-20T14:00:00Z"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"
        "500":
          $ref: "#/components/responses/InternalServerError"

    put:
      operationId: updateProduct
      summary: Update a product
      description: Replaces all fields of an existing product.
      tags:
        - Products
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ProductUpdate"
            example:
              name: "Wireless Bluetooth Headphones Pro"
              description: "Premium noise-cancelling wireless headphones with 40-hour battery life and aptX HD."
              price: 99.99
              currency: "USD"
              status: "active"
              category: "electronics"
              sku: "WBH-001-PRO"
              inventory_count: 200
              tags:
                - audio
                - wireless
                - premium
      responses:
        "200":
          description: Product updated successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"
              example:
                id: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"
                name: "Wireless Bluetooth Headphones Pro"
                slug: "wireless-bluetooth-headphones-pro"
                description: "Premium noise-cancelling wireless headphones with 40-hour battery life and aptX HD."
                price: 99.99
                currency: "USD"
                status: "active"
                category: "electronics"
                sku: "WBH-001-PRO"
                inventory_count: 200
                tags:
                  - audio
                  - wireless
                  - premium
                created_at: "2025-09-15T10:30:00Z"
                updated_at: "2025-10-01T09:15:00Z"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"
        "500":
          $ref: "#/components/responses/InternalServerError"

    delete:
      operationId: deleteProduct
      summary: Delete a product
      description: Permanently deletes a product from the catalog.
      tags:
        - Products
      responses:
        "204":
          description: Product deleted successfully
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"
        "500":
          $ref: "#/components/responses/InternalServerError"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from the authentication endpoint.
        Include in the Authorization header as: `Bearer <token>`

  schemas:
    Product:
      type: object
      description: A product in the catalog
      required:
        - id
        - name
        - slug
        - price
        - currency
        - status
        - created_at
        - updated_at
      properties:
        id:
          type: string
          description: Unique product identifier (ULID)
          example: "prod_01H8X3YKVB2N5FGJK0QW9TZRME"
          readOnly: true
        name:
          type: string
          description: Product display name
          minLength: 1
          maxLength: 255
          example: "Wireless Bluetooth Headphones"
        slug:
          type: string
          description: URL-safe identifier, auto-generated from name
          pattern: "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          example: "wireless-bluetooth-headphones"
          readOnly: true
        description:
          type: string
          description: Full product description
          maxLength: 5000
          example: "Premium noise-cancelling wireless headphones with 30-hour battery life."
        price:
          type: number
          format: double
          description: Product price
          minimum: 0
          example: 79.99
        currency:
          type: string
          description: ISO 4217 currency code
          pattern: "^[A-Z]{3}$"
          default: "USD"
          example: "USD"
        status:
          type: string
          description: Product visibility status
          enum:
            - active
            - draft
            - archived
          default: "draft"
          example: "active"
        category:
          type: string
          description: Category slug
          example: "electronics"
        sku:
          type: string
          description: Stock keeping unit
          maxLength: 100
          example: "WBH-001"
        inventory_count:
          type: integer
          description: Available inventory quantity
          minimum: 0
          default: 0
          example: 150
        tags:
          type: array
          description: Searchable tags
          items:
            type: string
          example:
            - audio
            - wireless
        created_at:
          type: string
          format: date-time
          description: Creation timestamp (ISO 8601)
          readOnly: true
          example: "2025-09-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          description: Last update timestamp (ISO 8601)
          readOnly: true
          example: "2025-09-20T14:00:00Z"

    ProductCreate:
      type: object
      description: Request body for creating a product
      required:
        - name
        - price
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
          example: "Wireless Bluetooth Headphones"
        description:
          type: string
          maxLength: 5000
          example: "Premium noise-cancelling wireless headphones with 30-hour battery life."
        price:
          type: number
          format: double
          minimum: 0
          example: 79.99
        currency:
          type: string
          pattern: "^[A-Z]{3}$"
          default: "USD"
          example: "USD"
        status:
          type: string
          enum:
            - active
            - draft
            - archived
          default: "draft"
          example: "draft"
        category:
          type: string
          example: "electronics"
        sku:
          type: string
          maxLength: 100
          example: "WBH-001"
        inventory_count:
          type: integer
          minimum: 0
          default: 0
          example: 150
        tags:
          type: array
          items:
            type: string
          example:
            - audio
            - wireless

    ProductUpdate:
      type: object
      description: Request body for updating a product
      required:
        - name
        - price
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
          example: "Wireless Bluetooth Headphones Pro"
        description:
          type: string
          maxLength: 5000
          example: "Premium noise-cancelling wireless headphones with 40-hour battery life and aptX HD."
        price:
          type: number
          format: double
          minimum: 0
          example: 99.99
        currency:
          type: string
          pattern: "^[A-Z]{3}$"
          example: "USD"
        status:
          type: string
          enum:
            - active
            - draft
            - archived
          example: "active"
        category:
          type: string
          example: "electronics"
        sku:
          type: string
          maxLength: 100
          example: "WBH-001-PRO"
        inventory_count:
          type: integer
          minimum: 0
          example: 200
        tags:
          type: array
          items:
            type: string
          example:
            - audio
            - wireless
            - premium

    PaginatedProductResponse:
      type: object
      description: Paginated list of products
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/Product"
        pagination:
          $ref: "#/components/schemas/Pagination"

    Pagination:
      type: object
      description: Pagination metadata
      required:
        - page
        - per_page
        - total
        - total_pages
        - has_next
        - has_prev
      properties:
        page:
          type: integer
          description: Current page number
          example: 1
        per_page:
          type: integer
          description: Items per page
          example: 20
        total:
          type: integer
          description: Total number of items
          example: 85
        total_pages:
          type: integer
          description: Total number of pages
          example: 5
        has_next:
          type: boolean
          description: Whether a next page exists
          example: true
        has_prev:
          type: boolean
          description: Whether a previous page exists
          example: false

    ErrorResponse:
      type: object
      description: Error response following RFC 7807 Problem Details
      required:
        - type
        - title
        - status
        - detail
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type
          example: "https://api.example.com/errors/not-found"
        title:
          type: string
          description: Short human-readable summary
          example: "Not Found"
        status:
          type: integer
          description: HTTP status code
          example: 404
        detail:
          type: string
          description: Human-readable explanation specific to this occurrence
          example: "Product with ID 'prod_01H8X3YKVB2N5FGJK0QW9TZRME' was not found."
        instance:
          type: string
          description: URI reference for the specific occurrence
          example: "/v1/products/prod_01H8X3YKVB2N5FGJK0QW9TZRME"
        errors:
          type: array
          description: Validation errors (present on 400 responses)
          items:
            type: object
            properties:
              field:
                type: string
                example: "price"
              message:
                type: string
                example: "must be greater than or equal to 0"

  responses:
    BadRequest:
      description: Invalid request parameters or body
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/errors/validation"
            title: "Bad Request"
            status: 400
            detail: "Request validation failed."
            instance: "/v1/products"
            errors:
              - field: "price"
                message: "must be greater than or equal to 0"
              - field: "name"
                message: "is required"

    Unauthorized:
      description: Missing or invalid authentication token
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/errors/unauthorized"
            title: "Unauthorized"
            status: 401
            detail: "Bearer token is missing or invalid."
            instance: "/v1/products"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/errors/not-found"
            title: "Not Found"
            status: 404
            detail: "The requested resource was not found."
            instance: "/v1/products/prod_nonexistent"

    InternalServerError:
      description: Unexpected server error
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/errors/internal"
            title: "Internal Server Error"
            status: 500
            detail: "An unexpected error occurred. Please try again later."
            instance: "/v1/products"
```
