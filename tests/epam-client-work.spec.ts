import { expect, test } from '@playwright/test';

test.describe('EPAM client work navigation', () => {
  test('navigates through Services and opens Client Work', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1200 });
    await page.goto('https://www.epam.com/', { waitUntil: 'domcontentloaded' });

    const servicesButton = page.getByRole('button', { name: /^Services$/i }).first();
    await expect(servicesButton).toBeVisible();
    await servicesButton.click({ force: true });

    const servicesLink = page.locator('header').getByRole('link', { name: /^Services$/i }).first();
    await expect(servicesLink).toBeVisible();
    await servicesLink.click({ force: true });

    await expect(page).toHaveURL(/\/services(\/|$)/i);

    const exploreClientWorkLink = page.getByRole('link', { name: /Explore Our Client Work/i }).first();
    await expect(exploreClientWorkLink).toBeVisible();
    await exploreClientWorkLink.click();

    const clientWorkText = page.getByText(/Client Work/i).first();
    await expect(clientWorkText).toBeVisible();
  });
});
