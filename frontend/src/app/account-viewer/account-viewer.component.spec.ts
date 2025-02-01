import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountViewerComponent } from './account-viewer.component';

describe('AccountViewerComponent', () => {
  let component: AccountViewerComponent;
  let fixture: ComponentFixture<AccountViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountViewerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccountViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
