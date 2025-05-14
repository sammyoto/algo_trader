import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotPageComponent } from './bot-page.component';

describe('BotPageComponent', () => {
  let component: BotPageComponent;
  let fixture: ComponentFixture<BotPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BotPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BotPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
