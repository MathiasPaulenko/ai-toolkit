---
name: prestashop-module
version: 1.0.0
author: Mathias Paulenko Echeverz
description: PrestaShop module development guide. Covers module structure, hooks, controllers, database schemas, payment modules, and overrides in PHP/Smarty.
tags: [prestashop, php, e-commerce, module, cms, payment]
role: prestashop-developer
model: any
trigger: When the user mentions PrestaShop, module development, hooks, overrides, Smarty, payment gateway, or PrestaShop controllers.
---

# PrestaShop Module Development

## 1. Module Structure

```
mymodule/
  mymodule.php          # Main module class (extends Module)
  config.xml            # Module metadata
  logo.png              # 32x32 icon
  README.md
  
  config/
    _front.yml          # Front controller routes
    _admin.yml          # Admin controller routes
    
  src/
    Controller/
      Admin/
        AdminMyModuleController.php
      Front/
        MyModuleFrontController.php
    Entity/
      MyEntity.php
    Repository/
      MyEntityRepository.php
    Form/
      MyModuleFormType.php
      
  views/
    templates/
      admin/
        configure.tpl / .html.twig
      front/
        my_page.tpl / .html.twig
    css/
    js/
    img/
    
  sql/
    install.php
    uninstall.php
    
  translations/
    es.php
    fr.php
    
  upgrade/
    upgrade-1.1.0.php
```

## 2. Main Module Class

```php
<?php
// mymodule.php
if (!defined('_PS_VERSION_')) {
    exit;
}

class MyModule extends Module
{
    public function __construct()
    {
        $this->name = 'mymodule';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'Mathias Paulenko Echeverz';
        $this->need_instance = 0;
        $this->ps_versions_compliancy = ['min' => '1.7.0.0', 'max' => '8.99.99'];
        $this->bootstrap = true;

        parent::__construct();

        $this->displayName = $this->l('My Module');
        $this->description = $this->l('Description of my module.');
    }

    public function install()
    {
        return parent::install()
            && $this->registerHook('displayHome')
            && $this->registerHook('displayHeader')
            && $this->installDb();
    }

    public function uninstall()
    {
        return parent::uninstall() && $this->uninstallDb();
    }

    private function installDb()
    {
        $sql = 'CREATE TABLE IF NOT EXISTS `' . _DB_PREFIX_ . 'mymodule_data` (
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(255) NOT NULL,
            `value` TEXT,
            PRIMARY KEY (`id`)
        ) ENGINE=' . _MYSQL_ENGINE_ . ' DEFAULT CHARSET=utf8mb4;';
        return Db::getInstance()->execute($sql);
    }

    private function uninstallDb()
    {
        return Db::getInstance()->execute('DROP TABLE IF EXISTS `' . _DB_PREFIX_ . 'mymodule_data`');
    }
}
```

## 3. Hooks

### Display Hooks

```php
public function hookDisplayHome($params)
{
    $this->context->smarty->assign([
        'my_var' => 'Hello from my module!',
    ]);
    return $this->display(__FILE__, 'views/templates/front/home_block.tpl');
}

public function hookDisplayHeader()
{
    $this->context->controller->addCSS($this->_path . 'views/css/mymodule.css');
    $this->context->controller->addJS($this->_path . 'views/js/mymodule.js');
}
```

### Action Hooks

```php
public function hookActionValidateOrder($params)
{
    $order = $params['order'];
    $customer = new Customer($order->id_customer);
    
    // Custom logic after order validation
    Db::getInstance()->insert('mymodule_data', [
        'name' => 'order_' . $order->id,
        'value' => json_encode([
            'customer_email' => $customer->email,
            'total' => $order->total_paid,
        ]),
    ]);
}
```

## 4. Admin Controller

```php
<?php
// src/Controller/Admin/AdminMyModuleController.php

namespace MyModule\Controller\Admin;

use PrestaShopBundle\Controller\Admin\FrameworkBundleAdminController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class AdminMyModuleController extends FrameworkBundleAdminController
{
    public function indexAction(Request $request): Response
    {
        $form = $this->createForm(MyModuleFormType::class);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $data = $form->getData();
            // Process form data
            $this->addFlash('success', $this->trans('Settings saved', 'Modules.Mymodule.Admin'));
        }

        return $this->render('@Modules/mymodule/views/templates/admin/configure.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

## 5. Payment Module

```php
class MyPaymentModule extends PaymentModule
{
    public function __construct()
    {
        parent::__construct();
        $this->name = 'mypayment';
        $this->tab = 'payments_gateways';
        $this->version = '1.0.0';
    }

    public function getPaymentOptions()
    {
        $paymentOption = new PaymentOption();
        $paymentOption->setCallToActionText($this->l('Pay with My Gateway'))
            ->setAction($this->context->link->getModuleLink($this->name, 'validation', [], true))
            ->setAdditionalInformation($this->fetch('module:mypayment/views/templates/hook/payment_option.tpl'));

        return [$paymentOption];
    }

    public function hookPaymentOptions($params)
    {
        if (!$this->active) {
            return;
        }
        if (!$this->checkCurrency($params['cart'])) {
            return;
        }
        return $this->getPaymentOptions();
    }
}
```

## 6. Smarty Templates

```smarty
{* views/templates/front/my_page.tpl *}
<div class="mymodule-block">
    <h2>{$my_var|escape:'html':'UTF-8'}</h2>
    {foreach from=$items item=item}
        <div class="item">
            <h3>{$item.name|escape:'html':'UTF-8'}</h3>
            <p>{$item.description|escape:'html':'UTF-8'}</p>
        </div>
    {/foreach}
</div>
```

## 7. Configuration and Translations

### Configuration

```php
// Save configuration
Configuration::updateValue('MYMODULE_API_KEY', 'secret_key');

// Retrieve configuration
$apiKey = Configuration::get('MYMODULE_API_KEY');
```

### Translations

```php
// In code
$this->l('Hello World');

// translations/es.php
$GLOBALS['$_MODULE']['mymodule_123abc'] = 'Hola Mundo';
```

## 8. Overrides (Use Sparingly)

```php
// override/classes/Cart.php
class Cart extends CartCore
{
    public function getProducts($refresh = false, $id_product = false, $id_country = null)
    {
        $products = parent::getProducts($refresh, $id_product, $id_country);
        
        // Custom modification
        foreach ($products as &$product) {
            $product['custom_field'] = MyModule::getCustomValue($product['id_product']);
        }
        
        return $products;
    }
}
```

## 9. Best Practices

- Use `Tools::safeOutput()` and `pSQL()` for output escaping and SQL sanitization.
- Use `Validate` class for input validation.
- Follow PrestaShop coding standards (PSR-2 for newer versions).
- Use `Hook::exec()` instead of direct class overrides when possible.
- Support multistore with `Shop::getContextShopID()`.
- Clear cache after configuration changes.
- Use `Db::getInstance()->insert()`/`update()`/`delete()` for safe queries.
