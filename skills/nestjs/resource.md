---
name: nestjs-resource
description: Generates a complete NestJS resource (Module, Controller, Service, DTOs, Entities) following clean architecture principles.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# NestJS Resource Generator

This skill creates a vertical slice for a feature in a NestJS application.

## Usage
Run `/nestjs-resource <ResourceName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of NestJS
2. **Fetch official docs**: Use `WebFetch` on the relevant NestJS documentation page (https://docs.nestjs.com/) for the feature being generated
3. **Verify patterns**: Confirm that decorators, DI patterns, and module structure are still current
4. **Use latest patterns**: If NestJS has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which NestJS version the code targets

## Structure
Creates `src/<resource-name>/`:
- `<name>.module.ts`: Module definition.
- `<name>.controller.ts`: API endpoints.
- `<name>.service.ts`: Business logic.
- `dto/create-<name>.dto.ts`: Validation for creation.
- `dto/update-<name>.dto.ts`: Validation for updates.
- `entities/<name>.entity.ts`: Database entity (TypeORM/Prisma).
- `<name>.service.spec.ts`: Unit tests.

## Standards
- **Validation**: Use `class-validator` and `class-transformer` in DTOs.
- **Dependency Injection**: Use constructor injection.
- **Swagger**: Decorate controllers and DTOs with `@ApiTags`, `@ApiOperation`, `@ApiProperty`.
- **Error Handling**: Use standard NestJS exceptions (`NotFoundException`, `BadRequestException`).

## Examples

### Controller
```typescript
import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';

@ApiTags('products')
@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Post()
  @ApiOperation({ summary: 'Create a new product' })
  @ApiResponse({ status: 201, description: 'The product has been successfully created.' })
  create(@Body() createProductDto: CreateProductDto) {
    return this.productsService.create(createProductDto);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get a product by id' })
  findOne(@Param('id') id: string) {
    return this.productsService.findOne(+id);
  }
}
```

### DTO
```typescript
import { IsString, IsNumber, IsPositive, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateProductDto {
  @ApiProperty({ example: 'Gaming Laptop' })
  @IsString()
  name: string;

  @ApiProperty({ example: 1299.99 })
  @IsNumber()
  @IsPositive()
  price: number;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsString()
  description?: string;
}
```

### Service
```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Product } from './entities/product.entity';
import { CreateProductDto } from './dto/create-product.dto';

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private productsRepository: Repository<Product>,
  ) {}

  async create(createProductDto: CreateProductDto): Promise<Product> {
    const product = this.productsRepository.create(createProductDto);
    return this.productsRepository.save(product);
  }

  async findOne(id: number): Promise<Product> {
    const product = await this.productsRepository.findOneBy({ id });
    if (!product) {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }
    return product;
  }
}
```
