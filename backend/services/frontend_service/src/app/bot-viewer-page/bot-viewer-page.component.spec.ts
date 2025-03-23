import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotViewerPageComponent } from './bot-viewer-page.component';

describe('BotViewerPageComponent', () => {
  let component: BotViewerPageComponent;
  let fixture: ComponentFixture<BotViewerPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BotViewerPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BotViewerPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
