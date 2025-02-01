import { TestBed } from '@angular/core/testing';
import { HeaderComponent } from './header.component';
import { HeaderComponentHarness } from './header.harness';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';

describe('HeaderComponent', () => {
  let harness: HeaderComponentHarness;

  beforeEach(async () => {
    // Configure TestBed for the standalone component
    await TestBed.configureTestingModule({
      declarations: [HeaderComponent], // Import standalone component
    }).compileComponents();

    const fixture = TestBed.createComponent(HeaderComponent);
    const loader = TestbedHarnessEnvironment.loader(fixture);
    harness = await loader.getHarness(HeaderComponentHarness);
  });

  it('should display the title', async () => {
    const title = await harness.getNavLinks();
    expect(title[0]).toBe('Home');
  });
});