<?php

class BarTest extends \PHPUnit_Framework_TestCase
{
    public function testMethodA()
    {
        $bar = new Bar();
        $bar->a();
    }
}

class Bar
{
    public function a()
    {
        $a = 5;

        return 'A';
    }

    public function b()
    {
        $b = 'abc';

        return 'B';
    }

    public function x()
    {
        $a = 7;
    }
}