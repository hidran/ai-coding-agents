---
name: react-component
description: Generates production-ready React components with TypeScript, tests (Vitest/Jest), Storybook stories, and Tailwind CSS.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch]
---

# React Component Generator

This skill generates a complete, production-grade React component structure.

## Usage
Run `/react-component <ComponentName>`

## Pre-Generation (MANDATORY)

Before generating any code, you MUST:
1. **Check latest version**: Use `WebSearch` to find the current stable version of React
2. **Fetch official docs**: Use `WebFetch` on the relevant React documentation page (https://react.dev/) for the feature being generated
3. **Verify patterns**: Confirm that hooks, component patterns, and testing approaches are still current
4. **Use latest patterns**: If React has introduced newer or better approaches (e.g., React Server Components, use() hook, React Compiler), prefer those over the examples below
5. **Note version**: Add a comment in generated code indicating which React version the code targets

## Structure
It will create a folder `src/components/<ComponentName>/` containing:
- `index.ts`: Barrel file
- `<ComponentName>.tsx`: Main component
- `<ComponentName>.test.tsx`: Unit tests
- `<ComponentName>.stories.tsx`: Storybook stories
- `<ComponentName>.types.ts`: TypeScript interfaces

## Standards
- **Functional Components**: Use `React.FC` or direct function definitions.
- **Hooks**: Use standard hooks (`useState`, `useEffect`) and custom hooks where appropriate.
- **Styling**: Tailwind CSS for styling.
- **Testing**: React Testing Library with user-event.
- **Accessibility**: Ensure proper ARIA attributes and keyboard navigation.

## Examples

### Component Implementation
```tsx
import React from 'react';
import { ComponentNameProps } from './ComponentName.types';

export const ComponentName: React.FC<ComponentNameProps> = ({ 
  label, 
  variant = 'primary', 
  onClick 
}) => {
  const baseStyles = 'px-4 py-2 rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  };

  return (
    <button
      type="button"
      className={`${baseStyles} ${variants[variant]}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};
```

### Test Example
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName label="Click me" />);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles clicks', () => {
    const handleClick = vi.fn();
    render(<ComponentName label="Click me" onClick={handleClick} />);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Storybook Example
```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

const meta: Meta<typeof ComponentName> = {
  title: 'Components/ComponentName',
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof ComponentName>;

export const Primary: Story = {
  args: {
    label: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    label: 'Secondary Button',
    variant: 'secondary',
  },
};
```
