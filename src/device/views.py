from django.shortcuts import render
from .utils import DH_Endpoint
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from device.models import Device, Miner
from device.serializers import DevSerializer, MinSerializer, GlobSerializer
import requests
from local.models import *
from django.contrib import messages
import random
import string



def cripto_connect(request):
    p_key = 7919
    device = Device.objects.get(public_key = p_key)
    content = requests.get('http://127.0.0.1:8002/cripto/19')
    gdata = content.json()
    context = {
        'par' : gdata['partial'],
    }
    device.partial = gdata['partial']
    device.save()
    miner =  Miner.objects.get(public_key = 19)
    med = DH_Endpoint(miner.public_key, p_key, miner.private_key)


    # add genesis block
    block = Block.objects.latest('id')
    print(block)
    try:
        policy = PolicyHeader.objects.get(
            requester = request.user,
            requested_action = PolicyHeader.GENESIS,
            device = device,
            action = PolicyHeader.ALLOW,
        )
        true = policy in block.policy_header.all()

    except:

        messages.warning(request, 'You don\'t have Permission to add this transaction')
        return HttpResponseRedirect(reverse('local:local'))

    else:

        device.dh_key = med.generate_full_key(device.partial)
        device.save()
        transaction = Transactions(
            transaction_number = 1,
            device = device,
            transaction_type = Transactions.GENESIS,
        )
        transaction.save()
        block.transactions.add(transaction)

        return HttpResponseRedirect(reverse('local:local'))


def alter(request, id):
    device = Device.objects.get(pk=id)
    block = Block.objects.latest('id')
    try:
        policy = PolicyHeader.objects.get(
            requester = request.user,
            requested_action = PolicyHeader.STORE,
            device = device,
            action = PolicyHeader.ALLOW,
        )
        true = policy in block.policy_header.all()
        print(true)

    except:

        messages.warning(request, 'You don\'t have Permission to add this transaction')
        return HttpResponseRedirect(reverse('local:local'))

    else:

        if not true:
            messages.warning(request, 'You don\'t have Permission to add this transaction')
            return HttpResponseRedirect(reverse('local:local'))


        p_transaction = Transactions.objects.filter(device=device).latest()
        if p_transaction.device_status == True:
            transaction = Transactions(
                prev_transaction = p_transaction,
                transaction_number = p_transaction.transaction_number+1,
                device = device,
                transaction_type = Transactions.STORE,
                device_status = False,
            )
        else:
            transaction = Transactions(
                prev_transaction=p_transaction,
                transaction_number=p_transaction.transaction_number + 1,
                device=device,
                transaction_type=Transactions.STORE,
                device_status=True,
            )
        transaction.save()
        if block.transactions.count() >= 5:
            def random_char(y):
                return ''.join(random.choice(string.ascii_lowercase) for x in range(y))

            header = BlockHeader(hash = random_char(20))
            header.save()

            new_block = Block(
                block_header = header,
                prev_block = block,
            )
            new_block.save()
            for p in block.policy_header.all():
                new_block.policy_header.add(p)
                new_block.save()

        block.transactions.add(transaction)

        return HttpResponseRedirect(reverse('local:local'))



@api_view(['GET'])
def partial(request, pk):
    miner = Miner.objects.get(public_key = 19)
    min = DH_Endpoint(miner.public_key, pk, miner.private_key)
    miner.partial = min.generate_partial_key()
    miner.save()
    print(miner.partial)
    serializer = MinSerializer(miner)
    return Response(serializer.data)


@api_view(['GET'])
def return_global(request, hash):
    num = BlockHeader.objects.all().count()
    print (num)
    print (hash)
    try:
        glo = BlockHeader.objects.all().order_by('-id')[:(num-hash)]
    except glo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GlobSerializer(glo, many=True)
    return Response(serializer.data)