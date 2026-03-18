---
name: angular-component
description: Generates production-ready Angular standalone components with signals, TypeScript, unit tests (Jasmine/Jest), and Storybook stories.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# Angular Component Generator

This skill generates a complete, production-grade Angular standalone component.

## Usage
Run `/angular-component <ComponentName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of Angular
2. **Fetch official docs**: Use `WebFetch` on the relevant Angular documentation page (https://angular.dev/) for the feature being generated
3. **Verify patterns**: Confirm that standalone components, signals, input()/output() APIs, and control flow syntax (@if, @for) shown in examples are still current
4. **Use latest patterns**: If Angular has introduced newer or better approaches, prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which Angular version the code targets

## Structure
Creates a folder `src/app/components/<component-name>/` containing:
- `<component-name>.component.ts`: Standalone component with signals
- `<component-name>.component.html`: Template
- `<component-name>.component.scss`: Styles
- `<component-name>.component.spec.ts`: Unit tests
- `<component-name>.component.stories.ts`: Storybook stories
- `index.ts`: Barrel file

## Standards
- **Standalone Components**: Always use `standalone: true`, no NgModules.
- **Signals**: Use Angular signals (`signal()`, `computed()`, `effect()`) instead of traditional change detection.
- **Input/Output**: Use `input()` and `output()` signal-based APIs (Angular 17+).
- **OnPush**: Always use `ChangeDetectionStrategy.OnPush`.
- **Typed Forms**: Use typed reactive forms when forms are involved.
- **Accessibility**: Proper ARIA attributes and keyboard navigation.
- **Testing**: Use Angular Testing Library or TestBed with Jasmine/Jest.

## Examples

### Component Implementation
```typescript
import { Component, ChangeDetectionStrategy, computed, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

export type ButtonVariant = 'primary' | 'secondary' | 'danger';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    '[class]': 'hostClasses()',
    '[attr.data-variant]': 'variant()',
  },
  template: `
    <button
      [type]="type()"
      [disabled]="disabled()"
      [class]="buttonClasses()"
      [attr.aria-disabled]="disabled()"
      [attr.aria-label]="ariaLabel()"
      (click)="handleClick()"
    >
      <ng-content />
      @if (loading()) {
        <span class="spinner" aria-hidden="true"></span>
      }
    </button>
  `,
  styles: [`
    :host { display: inline-block; }
    .btn { padding: 0.5rem 1rem; border-radius: 0.375rem; font-weight: 500; transition: background-color 0.2s; cursor: pointer; border: none; }
    .btn:focus-visible { outline: 2px solid var(--ring-color); outline-offset: 2px; }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-primary { background-color: #2563eb; color: #fff; --ring-color: #3b82f6; }
    .btn-primary:hover:not(:disabled) { background-color: #1d4ed8; }
    .btn-secondary { background-color: #e5e7eb; color: #111827; --ring-color: #6b7280; }
    .btn-secondary:hover:not(:disabled) { background-color: #d1d5db; }
    .btn-danger { background-color: #dc2626; color: #fff; --ring-color: #ef4444; }
    .btn-danger:hover:not(:disabled) { background-color: #b91c1c; }
    .spinner { display: inline-block; width: 1rem; height: 1rem; border: 2px solid currentColor; border-right-color: transparent; border-radius: 50%; animation: spin 0.6s linear infinite; margin-left: 0.5rem; }
    @keyframes spin { to { transform: rotate(360deg); } }
  `],
})
export class ButtonComponent {
  readonly variant = input<ButtonVariant>('primary');
  readonly disabled = input(false);
  readonly loading = input(false);
  readonly type = input<'button' | 'submit' | 'reset'>('button');
  readonly ariaLabel = input<string | undefined>(undefined);

  readonly clicked = output<MouseEvent>();

  readonly buttonClasses = computed(() => {
    return `btn btn-${this.variant()}`;
  });

  readonly hostClasses = computed(() => {
    return this.loading() ? 'is-loading' : '';
  });

  handleClick(): void {
    if (!this.disabled() && !this.loading()) {
      this.clicked.emit(new MouseEvent('click'));
    }
  }
}
```

### Template Example
```html
<!-- button.component.html (if using external template) -->
<button
  [type]="type()"
  [disabled]="disabled()"
  [class]="buttonClasses()"
  [attr.aria-disabled]="disabled()"
  [attr.aria-label]="ariaLabel()"
  (click)="handleClick()"
>
  <ng-content />
  @if (loading()) {
    <span class="spinner" aria-hidden="true"></span>
  }
</button>
```

### Test Example
```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Component } from '@angular/core';
import { ButtonComponent, ButtonVariant } from './button.component';

@Component({
  standalone: true,
  imports: [ButtonComponent],
  template: `
    <app-button
      [variant]="variant"
      [disabled]="disabled"
      [loading]="loading"
      (clicked)="onClick($event)"
    >
      {{ label }}
    </app-button>
  `,
})
class TestHostComponent {
  variant: ButtonVariant = 'primary';
  disabled = false;
  loading = false;
  label = 'Click me';
  onClick = jasmine.createSpy('onClick');
}

describe('ButtonComponent', () => {
  let fixture: ComponentFixture<TestHostComponent>;
  let host: TestHostComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestHostComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TestHostComponent);
    host = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should render with projected content', () => {
    const button = fixture.nativeElement.querySelector('button');
    expect(button.textContent.trim()).toBe('Click me');
  });

  it('should apply variant class', () => {
    const button = fixture.nativeElement.querySelector('button');
    expect(button.classList).toContain('btn-primary');

    host.variant = 'danger';
    fixture.detectChanges();
    expect(button.classList).toContain('btn-danger');
  });

  it('should emit clicked event', () => {
    const button = fixture.nativeElement.querySelector('button');
    button.click();
    expect(host.onClick).toHaveBeenCalledTimes(1);
  });

  it('should not emit when disabled', () => {
    host.disabled = true;
    fixture.detectChanges();
    const button = fixture.nativeElement.querySelector('button');
    button.click();
    expect(host.onClick).not.toHaveBeenCalled();
  });

  it('should show spinner when loading', () => {
    host.loading = true;
    fixture.detectChanges();
    const spinner = fixture.nativeElement.querySelector('.spinner');
    expect(spinner).toBeTruthy();
    expect(spinner.getAttribute('aria-hidden')).toBe('true');
  });

  it('should set aria-disabled attribute', () => {
    host.disabled = true;
    fixture.detectChanges();
    const button = fixture.nativeElement.querySelector('button');
    expect(button.getAttribute('aria-disabled')).toBe('true');
  });
});
```

### Storybook Example
```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { argsToTemplate } from '@storybook/angular';
import { ButtonComponent } from './button.component';

const meta: Meta<ButtonComponent> = {
  title: 'Components/Button',
  component: ButtonComponent,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
      description: 'Visual style variant of the button.',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled.',
    },
    loading: {
      control: 'boolean',
      description: 'Whether the button shows a loading spinner.',
    },
    type: {
      control: 'select',
      options: ['button', 'submit', 'reset'],
      description: 'HTML button type attribute.',
    },
  },
  render: (args) => ({
    props: args,
    template: `<app-button ${argsToTemplate(args)}>Button Label</app-button>`,
  }),
};

export default meta;
type Story = StoryObj<ButtonComponent>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    disabled: false,
    loading: false,
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    disabled: false,
    loading: false,
  },
};

export const Danger: Story = {
  args: {
    variant: 'danger',
    disabled: false,
    loading: false,
  },
};

export const Disabled: Story = {
  args: {
    variant: 'primary',
    disabled: true,
    loading: false,
  },
};

export const Loading: Story = {
  args: {
    variant: 'primary',
    disabled: false,
    loading: true,
  },
};
```

### Barrel File
```typescript
export { ButtonComponent } from './button.component';
export type { ButtonVariant } from './button.component';
```
