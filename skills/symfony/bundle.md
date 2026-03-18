---
name: symfony-bundle
description: Generates a Symfony bundle structure or a feature set (Entity, Repository, Controller, Form) within an existing app.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Symfony Feature Generator

This skill creates a cohesive set of classes for a feature in a Symfony application.

## Usage
Run `/symfony-feature <EntityName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Symfony
2. **Fetch official docs**: Use `WebFetch` on the relevant Symfony documentation page (https://symfony.com/doc/current/) for the feature being generated
3. **Verify patterns**: Confirm that attributes, dependency injection, and bundle structure are still current
4. **Use latest patterns**: If Symfony has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Symfony version the code targets

## Structure
Generates:
- `src/Entity/<EntityName>.php`: Doctrine entity.
- `src/Repository/<EntityName>Repository.php`: Repository class.
- `src/Controller/<EntityName>Controller.php`: Controller with attributes.
- `src/Form/<EntityName>Type.php`: Form definition.
- `tests/Controller/<EntityName>ControllerTest.php`: Functional tests.

## Standards
- **Attributes**: Use PHP 8 attributes for routing and ORM mapping.
- **Dependency Injection**: Use constructor injection.
- **Strict Types**: `declare(strict_types=1);` in all files.
- **DTOs**: Prefer DTOs for API inputs over direct Entity binding if complex.
- **Validation**: Use Symfony Validator constraints.

## Examples

### Entity
```php
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\ProductRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: ProductRepository::class)]
class Product
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    #[Assert\NotBlank]
    #[Assert\Length(min: 3)]
    private ?string $name = null;

    #[ORM\Column]
    #[Assert\PositiveOrZero]
    private ?int $price = null;

    // Getters and Setters...
}
```

### Controller
```php
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Product;
use App\Form\ProductType;
use App\Repository\ProductRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/product')]
class ProductController extends AbstractController
{
    #[Route('/', name: 'app_product_index', methods: ['GET'])]
    public function index(ProductRepository $productRepository): Response
    {
        return $this->render('product/index.html.twig', [
            'products' => $productRepository->findAll(),
        ]);
    }

    #[Route('/new', name: 'app_product_new', methods: ['GET', 'POST'])]
    public function new(Request $request, ProductRepository $productRepository): Response
    {
        $product = new Product();
        $form = $this->createForm(ProductType::class, $product);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $productRepository->save($product, true);

            return $this->redirectToRoute('app_product_index', [], Response::HTTP_SEE_OTHER);
        }

        return $this->render('product/new.html.twig', [
            'product' => $product,
            'form' => $form,
        ]);
    }
}
```

### Repository
```php
<?php

declare(strict_types=1);

namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<Product>
 */
class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }

    public function save(Product $entity, bool $flush = false): void
    {
        $this->getEntityManager()->persist($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }
}
```
