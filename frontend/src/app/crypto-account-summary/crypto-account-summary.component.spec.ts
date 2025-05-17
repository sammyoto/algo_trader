import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CryptoAccountSummaryComponent } from './crypto-account-summary.component';

describe('CryptoAccountSummaryComponent', () => {
  let component: CryptoAccountSummaryComponent;
  let fixture: ComponentFixture<CryptoAccountSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CryptoAccountSummaryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CryptoAccountSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
