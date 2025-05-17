import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrokerageAccountSummaryComponent } from './brokerage-account-summary.component';

describe('BrokerageAccountSummaryComponent', () => {
  let component: BrokerageAccountSummaryComponent;
  let fixture: ComponentFixture<BrokerageAccountSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BrokerageAccountSummaryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BrokerageAccountSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
