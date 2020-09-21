import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

export function getBaseUrl(): string {
  return document.getElementsByTagName('base')[0].href;
}

export function getApiUrl(): string {
  return "http://localhost:5000";
}

const providers = [
  { provide: "API_URL", useFactory: getApiUrl, deps: [] }
];

if (environment.production) {
  enableProdMode();
}

platformBrowserDynamic(providers).bootstrapModule(AppModule)
  .catch(err => console.error(err));
