import { greet } from '../src/index';

test('greet returns expected output', () => {
  expect(greet('Applied')).toBe('Hello, Applied!');
});
