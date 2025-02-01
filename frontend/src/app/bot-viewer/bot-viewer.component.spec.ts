import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotViewerComponent } from './bot-viewer.component';

describe('BotViewerComponent', () => {
  let component: BotViewerComponent;
  let fixture: ComponentFixture<BotViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BotViewerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BotViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
