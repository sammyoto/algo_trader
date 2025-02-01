import { ComponentHarness } from '@angular/cdk/testing';

export class HeaderComponentHarness extends ComponentHarness {
  // Match the component's selector
  static hostSelector = 'app-header';

  // Method to get nav
  async getNavLinks(): Promise<string[]> {
    const links = await this.locatorForAll('.nav-link')();
    return Promise.all(links.map(link => link.text()));
  }
}